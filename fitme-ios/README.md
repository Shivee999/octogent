# FITme Ayurveda module: drop into Xcode

Three data files and three Swift files. You get a "Ayurveda" screen with:
- **Traditional Ayurvedic options**: 168 classical options for 15 everyday complaints, English + Hindi.
- **Herb safety for my medicine**: search a medicine (generic name, Indian name like "paracetamol", or US brand) to see which herbs to be careful with.
- **Herb and product safety**: 113 herbs, formulations and bhasmas with sources.

All of it works offline and on-device, with no network calls, so your "100% private" promise holds.

## Easiest: one file

`FITmeAyurveda.swift` (about 1 MB) contains everything: the models, the data layer, the SwiftUI screens and all the data embedded as JSON. Drag that one file into Xcode, tick your app target, and show `AyurvedaHomeView().environmentObject(AyurvedaStore())`. You don't need the separate files below. Don't add both, or Xcode will report duplicate types.

It was compiled with Swift 6.1 in Swift 6 language mode (about 8 s to build) and tested: everything loads in about 0.2 s and all checks pass. Xcode may be slow to open this file because of the embedded data; you don't need to open it.

## Alternative: separate files (about 10 minutes)

1. **Add the data files.** In Xcode, drag `Resources/AyurvedaOTC.json`, `Resources/HerbSafety.json` and `Resources/Medicines.json` into your project navigator. In the dialog, tick **Copy items if needed** and tick your **app target**. Together they add about 1 MB to the app.
2. **Add the code.** Drag `Sources/AyurvedaModels.swift`, `Sources/AyurvedaData.swift` and `Sources/AyurvedaViews.swift` in the same way, ticking the app target.
3. **Show the screen.** Wherever you want it, for example as a new tab in your `TabView`:

   ```swift
   AyurvedaHomeView()
       .environmentObject(AyurvedaStore())
       .tabItem { Label("Ayurveda", systemImage: "leaf") }
   ```

   Create `AyurvedaStore()` once (for example as a `@StateObject` in your App struct) if you show the screen in more than one place.
4. **Run it.** If you see "Data not loaded", a JSON file isn't ticked for your app target: select the file, then in the right panel under Target Membership tick your app.

Requires iOS 16+. Works with Swift 5 and Swift 6 language modes.

## Hooking it to your medicine-label scanner

Your scanner already reads label text on-device. Pass that text in:

```swift
let found = data.medicines(inScannedText: recognisedText)   // e.g. "Metformin Hydrochloride Tablets IP 500 mg" → metformin
if let medicine = found.first {
    // push MedicineSafetyView(data: data, medicine: medicine)
}
```

Indian strips must print the generic name larger than the brand, so matching on the generic name works even though Indian brand names (Dolo, Glycomet) aren't in the data yet.

## What was tested

The data layer (`AyurvedaModels.swift` and `AyurvedaData.swift`) was compiled with Swift 6.1 and run against the real JSON:
- paracetamol → acetaminophen and frusemide → furosemide match correctly.
- A scanned Glycomet strip finds metformin.
- Warfarin shows 35 warnings, with 1 major (St John's wort).
- Metronidazole gets the arishta alcohol warnings, but other antibiotics don't.
- Phenytoin gets the shankhpushpi major warning, while valproate gets it as moderate.
- In total there are 13,180 warnings, exactly matching the Python build.
- Loading takes about 0.14 s.

The SwiftUI screens (`AyurvedaViews.swift`) couldn't be compiled here because SwiftUI only exists on Apple platforms. If Xcode flags anything, paste the error back and it's a quick fix.

## Updating the data later

From the repo: `python3 fitme-ayurveda-data/build_ayurveda.py`, then `build_otc_alternatives.py`, then `build_ios_data.py`, then `build_ios_single_file.py`. Drag the new JSON files in, replacing the old ones.

## Before release

- Keep the disclaimer visible on every result screen (the views already do this).
- In App Store text, say "traditional Ayurvedic options" and "herb safety information". Don't say "treats", "cures" or "alternative to your medicine".
- Have a Hindi reader skim the Devanagari names in `fitme-ayurveda-data/hindi_names.py`.
