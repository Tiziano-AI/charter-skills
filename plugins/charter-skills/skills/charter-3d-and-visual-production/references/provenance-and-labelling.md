# Provenance and Labelling

Provenance matters when source identity, reproducibility, rights, disclosure or variant lineage
matters to the product or its audience. Labelling matters when the asset will be published.

## Source classes

- **canonical reference:** accepted product or user source that locks identity, style, layout or
  geometry;
- **generation source:** the original selected model or provider output;
- **captured source:** camera, screenshot, scan, frame or product capture;
- **licensed source:** third-party asset with license and use constraints;
- **derived asset:** crop, resize, mask, composite, color transform, atlas, encode or poster made
  from a source;
- **inspection artifact:** contact sheet, preview, overlay or test render used for comparison;
- **package output:** the canonical file integrated or delivered for a product role.

Keep sources and derivatives distinguishable. A packaged file can be visually correct while its
reproduction path or rights remain unknown. Never present a derivative as the original generation
source, and keep the original before repairing it.

## Generation record

For each selected creative source, retain what applies:

- asset and variant identifier;
- prompt or creative brief;
- reference identities, each with the role it governed;
- model, provider, source or creator;
- generation settings, seed or job identifier when the provider exposes them;
- original output path and digest, and whether it carried Content Credentials or a watermark;
- when it was generated or selected;
- license, consent, attribution, disclosure or other usage constraint;
- why it was selected and its known limitations.

## Derivative and repair lineage

Record transformations when repeatability or diagnosis depends on them:

```text
source asset -> operation and parameters -> derived asset -> product role
```

Useful parameters include the crop rectangle, resize filter, density, color profile, mask or alpha
method, compression settings, extracted frame, video codec, atlas layout and composite inputs.

A repair record names the defective region or property, the intervention, the source used, the
resulting asset and the variants that need another look. Keep the canonical source unless a new
generation deliberately replaces it.

## Content Credentials and embedded source type

Content Credentials are C2PA manifests: signed statements about how an asset was created and
edited, stored in the file or beside it. A hard binding cryptographically connects the manifest
to the covered asset data. Changing that data invalidates the binding unless a C2PA-aware tool
records the edit in a new manifest that names the previous file as its ingredient. Tools and
platforms that do not support C2PA routinely drop the manifest when they resize, recompress or
convert. Soft bindings, an invisible watermark or a fingerprint, let a verifier look up a manifest
that became detached from its file; a watermark such as SynthID survives some transformations that
strip metadata, but not all of them.

For generated content a C2PA manifest can record a `c2pa.created` action with the IPTC digital
source type
`trainedAlgorithmicMedia`; a generative edit of a captured image is
`compositeWithTrainedAlgorithmicMedia`. Outside C2PA, the same vocabulary appears in XMP as
`Iptc4xmpExt:DigitalSourceType`.

[OpenAI's provenance verifier](https://developers.openai.com/api/docs/guides/content-provenance)
checks supported OpenAI C2PA signals in images and SynthID signals in images and audio. Coverage
depends on product, model, format and creation date; not every OpenAI-generated file has a
supported signal. Google's [Veo documentation](https://ai.google.dev/gemini-api/docs/veo#limitations)
states that Veo videos carry SynthID, but OpenAI's verifier is not a detector of other providers'
AI output.

Read a verification result at its actual scope. `detected` establishes a supported signal, not a
complete history, a prompt, an account or an individual creator. `not_detected` means no supported
signal was detected: it does not establish human authorship, absence of AI editing or absence of
OpenAI origin. Metadata stripping, watermark degradation, older models and transformations can
explain it. For C2PA, inspect `issuer` and `validation_state`; another issuer's manifest or an
invalid manifest can accompany `not_detected`. A manifest's presence alone does not mean it
records AI generation. Keep the source's credentials distinct from the delivered derivative's
observed state.

`c2patool <file>` prints the manifest a file carries.
`c2patool <derived> -m <manifest.json> -p <source> -o <signed>` writes a derivative whose manifest
names its source as parent; it needs a signer with a certificate the verifier will trust. Where the
pipeline cannot sign, record in the bundle whether each delivered file still carries credentials,
and do not describe a stripped derivative as credentialed.

## Platform labels

Platform detection and uploader disclosure are separate mechanisms. Their scopes differ:

- [YouTube](https://support.google.com/youtube/answer/14328491?hl=en) requires disclosure when AI
  meaningfully alters or generates photorealistic content:
  a real person appearing to say or do something they did not, altered footage of real events or
  places, or a realistic scene that did not occur. Non-realistic animation,
  minor aesthetic edits such as color or lighting, and production help such as scripts or thumbnails do
  not need it; AI-generated music that is the video's main focus also requires disclosure.
  YouTube may apply a label from its own AI tools, C2PA metadata or internal detection, and
  repeated non-disclosure can lead to penalties.
- Meta's [labelling approach](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/)
  distinguishes generated content from AI edits. Its
  [organic-media disclosure policy](https://about.fb.com/news/2024/02/labeling-ai-generated-images-on-facebook-instagram-and-threads/)
  describes detection of C2PA and IPTC AI indicators and requires
  people to use its disclosure tool when they post photorealistic video or realistic-sounding audio
  that was digitally created or altered.
- [TikTok](https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content)
  requires creators to label realistic AI-generated content and may automatically label content,
  including uploads with Content Credentials.

Keeping markers does not guarantee a particular label, and absent markers do not remove uploader
duties or prevent other detection. Read the destination's current policy when publication depends
on it, distinguishing organic posts from advertising and other separately governed placements.

## EU AI Act, Article 50

[Article 50](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50) of Regulation (EU)
2024/1689 distinguishes provider marking from deployer disclosure. It applies
from 2 August 2026. Under
[Article 111(4)](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-111),
providers of generative AI systems placed on the market before that date must
comply with Article 50(2) by 2 December 2026. This transition concerns provider
marking, not deployer disclosure under Article 50(4). Check the applicable
legal text for the system and publication concerned.
It reaches providers who place
systems on the EU market wherever they are established, deployers established or located in the
Union, and providers and deployers elsewhere whose system output is used in the Union. A natural
person using an AI system for a purely personal, non-professional
activity is not a deployer.

- **Providers mark (50(2)).** Providers of systems that generate synthetic audio, image, video or
  text must mark outputs in a machine-readable format detectable as artificially generated or
  manipulated, except for assistive standard editing or edits that do not substantially alter the
  input. A transitional rule for provider marking does not by itself defer
  deployer disclosure. Producing an asset with someone else's system does not
  itself make the asset producer the system's provider.
- **Deployers disclose deep fakes (50(4)).** A deep fake is AI-generated or manipulated image, audio
  or video content that resembles existing persons, objects, places, entities or events and would
  falsely appear to a person to be authentic or truthful. Whoever deploys the system that produces
  it must disclose that the content is artificially generated or manipulated. When the content is
  part of an evidently artistic, creative, satirical, fictional or analogous work, the duty shrinks
  to disclosing the existence of generated content in an appropriate manner that does not hamper
  the display or enjoyment of the work. AI-generated text published to inform the public on matters
  of public interest must also be disclosed, unless it underwent human review or editorial control
  and someone holds editorial responsibility.
- **How to disclose (50(5)).** The information must be clear and distinguishable, given at the
  latest at the first interaction or exposure, and meet accessibility requirements.
  Embedded machine-readable marks alone do not discharge the audience-facing deployer duty.

The Commission and the AI Board have confirmed the final
[Code of Practice on Transparency of AI-generated Content](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)
as an adequate voluntary tool to demonstrate compliance with the transparency
obligations under Articles 50(2), (4) and (5). Following the Code is voluntary;
the underlying legal obligations are not. Its implementation guidance explains
the compliance route and audience-facing labels. Using an icon alone is not
equivalent to following the Code.

The [Commission's Article 50 FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)
interprets deepfake classification through three cumulative conditions: high resemblance to the
simulated subject; a subject that exists, could plausibly exist or could plausibly have existed;
and a false appearance of authenticity or truthfulness. The last depends on the message,
foreseeable placement and audience expectations. Photorealism alone does not establish a
deepfake, and fictional intent alone does not exclude one.

A realistic generated image of an invented event in a named city square qualifies when presented
so viewers could mistake it for a real occurrence. An unmistakably fantastical landscape or
stylized mascot will ordinarily fail those conditions, but style is not a blanket exemption.
An evidently artistic work that does qualify still needs disclosure in a manner that preserves
its display and enjoyment. For an ambiguous product composite or campaign scene, retain the
contextual classification and its decision owner with the asset; settle the audience-facing
placement separately from embedded provenance.

## Bundle manifest

A large bundle or several contributors need one manifest; a single asset needs a source note. Adapt
the fields to the bundle and omit what does not apply:

```json
{
  "bundle": "onboarding-illustrations",
  "outputs": [
    {
      "role": "welcome-hero",
      "path": "final/welcome-hero.webp",
      "sha256": "…",
      "format": "webp, lossless alpha",
      "dimensions": "…",
      "variants": ["light", "dark"],
      "source": "selected/welcome-hero-base.png",
      "transformations": ["crop to hero safe area", "alpha edge cleanup", "encode"],
      "content_credentials": "stripped by encode; original output keeps them",
      "disclosure": "no deepfake disclosure for this placement: unmistakably fictional onboarding art, not presented as a real occurrence; destination policy checked",
      "destination": "app asset catalog",
      "known_limitations": []
    }
  ],
  "sources": [
    {
      "id": "welcome-hero-base",
      "brief": "prompts/welcome-hero.txt",
      "references": [{"path": "refs/mascot.png", "role": "identity"}],
      "generator": "provider and model",
      "settings": "as exposed by the provider",
      "selected_because": "clear silhouette at hero size, quiet region for the headline"
    }
  ],
  "open_repairs": [
    {
      "asset": "welcome-hero/dark",
      "defect": "light fringe on the lower edge against dark backgrounds",
      "intervention": "deterministic alpha-edge cleanup from the selected source",
      "reinspect": ["welcome-hero/light"]
    }
  ],
  "excluded_from_runtime": ["rejected candidates", "contact sheets", "repair intermediates"]
}
```

Add inspection notes per output (contexts seen, select, repair or reject, remaining defects) when
several reviewers share the selection. Use digests when exact bytes matter across generation,
packaging and integration. For motion, record duration, frame rate and loop points.
