import AppKit
import SwiftUI

// macOS has no Dynamic Type. The counter offers its own text scale (View ›
// Larger Text) for people reading it from further away. At 1× every role uses
// a system text style; at a larger scale it uses that style's Mac size
// multiplied by the scale, so the hierarchy keeps its proportions.

struct ContentTextScaleKey: EnvironmentKey {
    static let defaultValue: CGFloat = 1
}

extension EnvironmentValues {
    var contentTextScale: CGFloat {
        get { self[ContentTextScaleKey.self] }
        set { self[ContentTextScaleKey.self] = newValue }
    }
}

extension Font.TextStyle {
    var appKitStyle: NSFont.TextStyle {
        switch self {
        case .largeTitle: .largeTitle
        case .title: .title1
        case .title2: .title2
        case .title3: .title3
        case .headline: .headline
        case .subheadline: .subheadline
        case .callout: .callout
        case .footnote: .footnote
        case .caption: .caption1
        case .caption2: .caption2
        default: .body
        }
    }

    /// The Mac's Headline is bold; the other styles are regular.
    var macWeight: Font.Weight { self == .headline ? .bold : .regular }

    var macPointSize: CGFloat { NSFont.preferredFont(forTextStyle: appKitStyle).pointSize }
}

struct ScaledTextStyle: ViewModifier {
    @Environment(\.contentTextScale) private var scale
    let style: Font.TextStyle
    let weight: Font.Weight?
    let design: Font.Design?

    func body(content: Content) -> some View {
        if scale == 1 {
            content.font(.system(style, design: design, weight: weight))
        } else {
            content.font(.system(size: style.macPointSize * scale, weight: weight ?? style.macWeight,
                                 design: design ?? .default))
        }
    }
}

extension View {
    func textStyle(_ style: Font.TextStyle, weight: Font.Weight? = nil, design: Font.Design? = nil) -> some View {
        modifier(ScaledTextStyle(style: style, weight: weight, design: design))
    }
}
