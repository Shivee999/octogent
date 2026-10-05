import Foundation

/// Loads the bundled Ayurveda JSON files and answers lookups. Pure Foundation, no UI,
/// so it can run off the main thread and be unit-tested.
struct AyurvedaData {
    let otc: OTCFile
    let herbFile: HerbFile
    let medicines: [Medicine]

    /// Normalised name or alias -> indices into `medicines`.
    private let nameIndex: [String: [Int]]
    /// Longest names first, for finding a medicine inside scanned label text.
    private let namesByLength: [String]

    enum LoadError: Error { case missingResource(String) }

    init(bundle: Bundle = .main) throws {
        func data(_ name: String) throws -> Data {
            guard let url = bundle.url(forResource: name, withExtension: "json") else {
                throw LoadError.missingResource("\(name).json")
            }
            return try Data(contentsOf: url)
        }
        try self.init(otcData: data("AyurvedaOTC"), herbData: data("HerbSafety"), medicineData: data("Medicines"))
    }

    init(otcData: Data, herbData: Data, medicineData: Data) throws {
        let decoder = JSONDecoder()
        otc = try decoder.decode(OTCFile.self, from: otcData)
        herbFile = try decoder.decode(HerbFile.self, from: herbData)
        medicines = try decoder.decode(MedicineFile.self, from: medicineData).medicines

        var index: [String: [Int]] = [:]
        for (i, m) in medicines.enumerated() {
            for name in [m.id, m.name] + m.aliases {
                let key = Self.normalise(name)
                guard key.count >= 3 else { continue }
                if index[key]?.contains(i) != true { index[key, default: []].append(i) }
            }
        }
        nameIndex = index
        namesByLength = index.keys.sorted { $0.count > $1.count }
    }

    var herbs: [Herb] { herbFile.herbs }
    var disclaimer: String { herbFile.disclaimer }

    func label(for drugClass: String) -> String {
        herbFile.drugClassLabels[drugClass] ?? drugClass
    }

    // MARK: Medicine search

    static func normalise(_ text: String) -> String {
        let folded = text.folding(options: [.caseInsensitive, .diacriticInsensitive], locale: nil)
        let cleaned = folded.unicodeScalars.map { CharacterSet.alphanumerics.contains($0) ? Character($0) : " " }
        return String(cleaned).split(separator: " ").joined(separator: " ")
    }

    /// Type-ahead search: names starting with the query first, then names containing it.
    func searchMedicines(_ query: String, limit: Int = 25) -> [Medicine] {
        let q = Self.normalise(query)
        guard q.count >= 2 else { return [] }
        var seen = Set<Int>()
        var prefix: [Int] = []
        var contains: [Int] = []
        for (key, ids) in nameIndex {
            if key.hasPrefix(q) {
                for i in ids where seen.insert(i).inserted { prefix.append(i) }
            } else if key.contains(q) {
                for i in ids where seen.insert(i).inserted { contains.append(i) }
            }
        }
        let byName: (Int, Int) -> Bool = { medicines[$0].name.count < medicines[$1].name.count }
        return (prefix.sorted(by: byName) + contains.sorted(by: byName)).prefix(limit).map { medicines[$0] }
    }

    /// Finds medicines named in text read from a strip or box (on-device OCR).
    /// Indian labels print the generic name prominently (Drugs Rules 1945, Rule 96).
    func medicines(inScannedText text: String) -> [Medicine] {
        let haystack = " " + Self.normalise(text) + " "
        var found: [Int] = []
        var covered = haystack
        for key in namesByLength where key.count >= 4 {
            let needle = " " + key + " "
            guard let range = covered.range(of: needle) else { continue }
            for i in nameIndex[key] ?? [] where !found.contains(i) { found.append(i) }
            // Blank out the match so "metformin" is not found again inside a longer name.
            covered.replaceSubrange(range, with: String(repeating: " ", count: needle.count))
        }
        return found.map { medicines[$0] }
    }

    // MARK: Herb warnings for a medicine

    func warnings(for medicine: Medicine) -> [HerbWarning] {
        let classes = Set(medicine.classes)
        guard !classes.isEmpty else { return [] }
        var result: [HerbWarning] = []
        for herb in herbs {
            var best: HerbWarning?
            for it in herb.interactions where classes.contains(it.drugClass) {
                if let only = it.onlyMolecules, !only.contains(medicine.id) { continue }
                var severity = it.severity
                if let majors = it.majorOnlyFor, !majors.contains(medicine.id), severity == .major {
                    severity = .moderate
                }
                if best == nil || severity > best!.severity {
                    best = HerbWarning(herb: herb, interaction: it, severity: severity)
                }
            }
            if let best { result.append(best) }
        }
        return result.sorted {
            $0.severity != $1.severity ? $0.severity > $1.severity : $0.herb.name < $1.herb.name
        }
    }

    /// Warnings grouped for display: severity, then drug class within it.
    func groupedWarnings(for medicine: Medicine) -> [(severity: Severity, groups: [(drugClass: String, warnings: [HerbWarning])])] {
        let all = warnings(for: medicine)
        return Severity.allCases.sorted(by: >).compactMap { sev in
            let items = all.filter { $0.severity == sev }
            guard !items.isEmpty else { return nil }
            let byClass = Dictionary(grouping: items, by: { $0.interaction.drugClass })
            let groups = byClass.keys.sorted { label(for: $0) < label(for: $1) }.map { (drugClass: $0, warnings: byClass[$0]!) }
            return (severity: sev, groups: groups)
        }
    }

    // MARK: Herbs and complaints

    func searchHerbs(_ query: String) -> [Herb] {
        let q = Self.normalise(query)
        guard !q.isEmpty else { return herbs }
        return herbs.filter { h in
            let names = [h.id, h.name, h.nameHi ?? "", h.sanskrit ?? "", h.latin ?? ""] + h.otherNames + h.commonProducts
            return names.contains { Self.normalise($0).contains(q) || $0.contains(query) }
        }
    }

    func searchComplaints(_ query: String) -> [OTCComplaint] {
        let q = Self.normalise(query)
        guard !q.isEmpty else { return otc.complaints }
        return otc.complaints.filter { c in
            Self.normalise(c.title).contains(q) || (c.titleHi ?? "").contains(query)
                || Self.normalise(c.otcMedicinesUsuallyUsed).contains(q)
                || c.options.contains { Self.normalise($0.name).contains(q) || ($0.nameHi ?? "").contains(query) }
        }
    }
}
