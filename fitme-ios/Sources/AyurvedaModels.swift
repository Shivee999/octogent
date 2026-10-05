import Foundation

// MARK: - Ayurvedic options for minor complaints (AyurvedaOTC.json)

struct OTCFile: Decodable {
    let version: String
    let disclaimer: String
    let complaints: [OTCComplaint]
}

struct OTCComplaint: Decodable, Identifiable, Hashable {
    let id: String
    let title: String
    let titleHi: String?
    let otcMedicinesUsuallyUsed: String
    let seeADoctorIf: String
    let source: String
    let options: [OTCOption]
}

struct OTCOption: Decodable, Identifiable, Hashable {
    let id: String
    let name: String
    let nameHi: String?
    let form: String
    let howUsed: String
    let caution: String
}

// MARK: - Herb safety (HerbSafety.json)

struct HerbFile: Decodable {
    let version: String
    let disclaimer: String
    let drugClassLabels: [String: String]
    let herbs: [Herb]
}

enum Severity: String, Decodable, Comparable, CaseIterable {
    case major, moderate, minor

    var rank: Int {
        switch self {
        case .major: return 3
        case .moderate: return 2
        case .minor: return 1
        }
    }

    var title: String {
        switch self {
        case .major: return "Major"
        case .moderate: return "Moderate"
        case .minor: return "Minor"
        }
    }

    var subtitle: String {
        switch self {
        case .major: return "Avoid unless your doctor says it's fine"
        case .moderate: return "Check with your doctor first"
        case .minor: return "Lower-evidence interactions"
        }
    }

    static func < (lhs: Severity, rhs: Severity) -> Bool { lhs.rank < rhs.rank }
}

struct Herb: Decodable, Identifiable, Hashable {
    let id: String
    let name: String
    let nameHi: String?
    let sanskrit: String?
    let latin: String?
    let otherNames: [String]
    let kind: String
    let dataQuality: String
    let traditionalContext: String?
    let isAyurvedic: Bool
    let commonProducts: [String]
    let safetyFlags: [SafetyFlag]
    let interactions: [Interaction]
    let herbWarnings: [HerbLevelWarning]

    var kindLabel: String {
        switch kind {
        case "herb": return "Herb"
        case "food_spice": return "Spice / food"
        case "formulation": return "Formulation"
        case "mineral_preparation": return "Bhasma / mineral"
        default: return kind
        }
    }
}

struct SafetyFlag: Decodable, Hashable {
    let flag: String
    let note: String
    let evidence: String
    let sources: [String]
}

struct Interaction: Decodable, Hashable {
    let drugClass: String
    let severity: Severity
    let effect: String
    let mechanism: String?
    let evidence: String?
    let advice: String?
    let sources: [String]
    /// When set, this interaction applies only to these molecules, not the whole class.
    let onlyMolecules: [String]?
    /// When set, only these molecules get "major"; the rest of the class gets "moderate".
    let majorOnlyFor: [String]?
}

struct HerbLevelWarning: Decodable, Hashable {
    let severity: Severity
    let effect: String
    let sources: [String]
}

// MARK: - Medicines (Medicines.json)

struct MedicineFile: Decodable {
    let version: String
    let medicines: [Medicine]
}

struct Medicine: Decodable, Identifiable, Hashable {
    /// Lower-case generic molecule name, e.g. "warfarin".
    let id: String
    let name: String
    let classes: [String]
    let aliases: [String]
    let inNLEM: Bool
}

// MARK: - Result of matching a medicine against herbs

struct HerbWarning: Identifiable, Hashable {
    let herb: Herb
    let interaction: Interaction
    /// Severity after molecule-specific rules were applied.
    let severity: Severity

    var id: String { herb.id + "|" + interaction.drugClass }
}
