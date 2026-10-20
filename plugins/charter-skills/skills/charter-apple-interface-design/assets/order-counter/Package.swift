// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "OrderCounter",
    platforms: [.macOS(.v14)],
    targets: [.executableTarget(name: "OrderCounter", path: "Sources")]
)
