import SwiftUI

// MARK: - Store

/// Loads the bundled JSON once, off the main thread. Inject at the app root:
///   AyurvedaHomeView().environmentObject(AyurvedaStore())
@MainActor
final class AyurvedaStore: ObservableObject {
    @Published private(set) var data: AyurvedaData?
    @Published private(set) var loadError: String?

    init() {
        Task { await load() }
    }

    func load() async {
        do {
            let loaded = try await Task.detached(priority: .userInitiated) { try AyurvedaData() }.value
            data = loaded
        } catch {
            loadError = "Couldn't load Ayurveda data (\(error)). Check the JSON files are in the app target."
        }
    }
}

// MARK: - Home

struct AyurvedaHomeView: View {
    @EnvironmentObject private var store: AyurvedaStore

    var body: some View {
        NavigationStack {
            Group {
                if let data = store.data {
                    List {
                        Section {
                            NavigationLink {
                                ComplaintListView(data: data)
                            } label: {
                                HomeRow(title: "Traditional Ayurvedic options",
                                        subtitle: "For \(data.otc.complaints.count) everyday complaints",
                                        hindi: "आयुर्वेदिक पारंपरिक विकल्प", systemImage: "leaf")
                            }
                            NavigationLink {
                                MedicineSearchView(data: data)
                            } label: {
                                HomeRow(title: "Herb safety for my medicine",
                                        subtitle: "Which herbs to be careful with",
                                        hindi: "मेरी दवा के साथ जड़ी-बूटी सुरक्षा", systemImage: "pills")
                            }
                            NavigationLink {
                                HerbListView(data: data)
                            } label: {
                                HomeRow(title: "Herb and product safety",
                                        subtitle: "\(data.herbs.count) herbs, formulations and bhasmas",
                                        hindi: "जड़ी-बूटी और उत्पाद सुरक्षा", systemImage: "list.bullet.rectangle")
                            }
                        }
                        Section {
                            DisclaimerText(text: data.disclaimer)
                        }
                    }
                } else if let error = store.loadError {
                    ContentUnavailableCompat(title: "Data not loaded", message: error)
                } else {
                    ProgressView("Loading…")
                }
            }
            .navigationTitle("Ayurveda")
        }
    }
}

private struct HomeRow: View {
    let title: String
    let subtitle: String
    let hindi: String
    let systemImage: String

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: systemImage).font(.title3).foregroundStyle(.green).frame(width: 28)
            VStack(alignment: .leading, spacing: 2) {
                Text(title).font(.headline)
                Text(hindi).font(.subheadline).foregroundStyle(.secondary)
                Text(subtitle).font(.caption).foregroundStyle(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

// MARK: - Complaints → classical options

struct ComplaintListView: View {
    let data: AyurvedaData
    @State private var query = ""

    var body: some View {
        List(data.searchComplaints(query)) { complaint in
            NavigationLink {
                ComplaintDetailView(complaint: complaint, disclaimer: data.otc.disclaimer)
            } label: {
                VStack(alignment: .leading, spacing: 2) {
                    Text(complaint.title).font(.body.weight(.semibold))
                    if let hi = complaint.titleHi { Text(hi).font(.subheadline).foregroundStyle(.secondary) }
                    Text("\(complaint.options.count) options").font(.caption).foregroundStyle(.secondary)
                }
            }
        }
        .searchable(text: $query, prompt: "Search: acidity, खांसी, triphala…")
        .navigationTitle("Everyday complaints")
    }
}

struct ComplaintDetailView: View {
    let complaint: OTCComplaint
    let disclaimer: String

    var body: some View {
        List {
            Section {
                DisclaimerText(text: disclaimer)
            }
            Section("Usually treated with (OTC)") {
                Text(complaint.otcMedicinesUsuallyUsed).font(.subheadline)
            }
            Section("Traditional Ayurvedic options") {
                ForEach(complaint.options) { option in
                    OptionRow(option: option)
                }
            }
            Section {
                Label {
                    Text("See a doctor if: \(complaint.seeADoctorIf)").font(.subheadline)
                } icon: {
                    Image(systemName: "exclamationmark.triangle.fill").foregroundStyle(.red)
                }
            }
            Section("Source") {
                Text(complaint.source).font(.caption).foregroundStyle(.secondary).textSelection(.enabled)
            }
        }
        .navigationTitle(complaint.title)
        .navigationBarTitleDisplayMode(.inline)
    }
}

private struct OptionRow: View {
    let option: OTCOption
    @State private var expanded = false

    var body: some View {
        DisclosureGroup(isExpanded: $expanded) {
            Text(option.caution).font(.footnote).foregroundStyle(.secondary).padding(.vertical, 4)
        } label: {
            VStack(alignment: .leading, spacing: 2) {
                Text(option.name).font(.body.weight(.medium))
                if let hi = option.nameHi { Text(hi).font(.subheadline).foregroundStyle(.secondary) }
                Text("\(option.form) · \(option.howUsed)").font(.caption).foregroundStyle(.secondary)
            }
        }
    }
}

// MARK: - Medicine → herb warnings

struct MedicineSearchView: View {
    let data: AyurvedaData
    @State private var query = ""

    var body: some View {
        List {
            if query.count < 2 {
                Section {
                    Text("Type the generic name printed on your strip, e.g. metformin, paracetamol, amlodipine.")
                        .font(.subheadline).foregroundStyle(.secondary)
                }
            } else {
                let results = data.searchMedicines(query)
                if results.isEmpty {
                    Text("No medicine found. Try the generic name printed under the brand name.")
                        .foregroundStyle(.secondary)
                }
                ForEach(results) { medicine in
                    NavigationLink {
                        MedicineSafetyView(data: data, medicine: medicine)
                    } label: {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(medicine.name.capitalized).font(.body.weight(.medium))
                            Text(medicine.classes.isEmpty ? "No known herb interactions in our data"
                                 : medicine.classes.map(data.label(for:)).joined(separator: " · "))
                                .font(.caption).foregroundStyle(.secondary).lineLimit(2)
                        }
                    }
                }
            }
        }
        .searchable(text: $query, prompt: "Search a medicine")
        .autocorrectionDisabled()
        .navigationTitle("My medicine")
    }
}

struct MedicineSafetyView: View {
    let data: AyurvedaData
    let medicine: Medicine

    var body: some View {
        let grouped = data.groupedWarnings(for: medicine)
        List {
            Section {
                VStack(alignment: .leading, spacing: 6) {
                    Text(medicine.name.capitalized).font(.title2.bold())
                    if !medicine.classes.isEmpty {
                        Text(medicine.classes.map(data.label(for:)).joined(separator: " · "))
                            .font(.subheadline).foregroundStyle(.secondary)
                    }
                }
                DisclaimerText(text: data.disclaimer)
            }
            if grouped.isEmpty {
                Section {
                    Text("No known herb interactions in our data. That doesn't mean a combination is safe. Ask your pharmacist before adding any herbal product.")
                        .font(.subheadline)
                }
            }
            ForEach(grouped, id: \.severity) { block in
                Section {
                    if block.severity == .minor {
                        DisclosureGroup("Show \(block.groups.reduce(0) { $0 + $1.warnings.count }) lower-evidence interactions") {
                            warningRows(block.groups)
                        }
                    } else {
                        warningRows(block.groups)
                    }
                } header: {
                    SeverityHeader(severity: block.severity)
                }
            }
        }
        .navigationTitle(medicine.name.capitalized)
        .navigationBarTitleDisplayMode(.inline)
    }

    @ViewBuilder
    private func warningRows(_ groups: [(drugClass: String, warnings: [HerbWarning])]) -> some View {
        ForEach(groups, id: \.drugClass) { group in
            if groups.count > 1 {
                Text(data.label(for: group.drugClass)).font(.caption.weight(.semibold)).foregroundStyle(.secondary)
            }
            ForEach(group.warnings) { warning in
                NavigationLink {
                    HerbDetailView(data: data, herb: warning.herb)
                } label: {
                    WarningRow(warning: warning)
                }
            }
        }
    }
}

private struct SeverityHeader: View {
    let severity: Severity

    var body: some View {
        HStack(spacing: 8) {
            Text(severity.title.uppercased())
                .font(.caption2.bold())
                .padding(.horizontal, 6).padding(.vertical, 2)
                .background(severity.color.opacity(0.18), in: RoundedRectangle(cornerRadius: 4))
                .foregroundStyle(severity.color)
            Text(severity.subtitle).font(.caption)
        }
    }
}

private struct WarningRow: View {
    let warning: HerbWarning

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack(alignment: .firstTextBaseline) {
                Text(warning.herb.name).font(.body.weight(.semibold))
                if let hi = warning.herb.nameHi { Text(hi).font(.subheadline).foregroundStyle(.secondary) }
            }
            Text(warning.interaction.effect).font(.subheadline)
            if let advice = warning.interaction.advice {
                Text(advice).font(.caption).foregroundStyle(.secondary)
            }
            if let evidence = warning.interaction.evidence {
                Text("Evidence: \(evidence.replacingOccurrences(of: "_", with: " "))")
                    .font(.caption2).foregroundStyle(.secondary)
            }
        }
        .padding(.vertical, 2)
    }
}

// MARK: - Herbs

struct HerbListView: View {
    let data: AyurvedaData
    @State private var query = ""

    var body: some View {
        List(data.searchHerbs(query)) { herb in
            NavigationLink {
                HerbDetailView(data: data, herb: herb)
            } label: {
                VStack(alignment: .leading, spacing: 2) {
                    HStack(alignment: .firstTextBaseline) {
                        Text(herb.name).font(.body.weight(.medium))
                        if let hi = herb.nameHi { Text(hi).font(.subheadline).foregroundStyle(.secondary) }
                    }
                    Text("\(herb.kindLabel) · \(herb.interactions.count) interactions · data: \(herb.dataQuality)")
                        .font(.caption).foregroundStyle(.secondary)
                }
            }
        }
        .searchable(text: $query, prompt: "Search: ashwagandha, गिलोय, Liv.52…")
        .navigationTitle("Herbs")
    }
}

struct HerbDetailView: View {
    let data: AyurvedaData
    let herb: Herb

    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 4) {
                    if let hi = herb.nameHi { Text(hi).font(.title3) }
                    if let latin = herb.latin { Text(latin).font(.subheadline).italic().foregroundStyle(.secondary) }
                    Text("\(herb.kindLabel) · evidence quality: \(herb.dataQuality)").font(.caption).foregroundStyle(.secondary)
                }
                if let context = herb.traditionalContext {
                    Text(context + (herb.isAyurvedic ? "" : " (Not an Ayurvedic herb; listed because it is often sold alongside Ayurvedic products.)"))
                        .font(.subheadline)
                }
                DisclaimerText(text: data.disclaimer)
            }
            if !herb.herbWarnings.isEmpty {
                Section("Important") {
                    ForEach(herb.herbWarnings, id: \.self) { w in
                        Label(w.effect, systemImage: "exclamationmark.octagon.fill")
                            .foregroundStyle(w.severity.color)
                    }
                }
            }
            if !herb.safetyFlags.isEmpty {
                Section("Safety") {
                    ForEach(herb.safetyFlags, id: \.self) { flag in
                        VStack(alignment: .leading, spacing: 2) {
                            Text(flag.flag.replacingOccurrences(of: "_", with: " ").capitalized).font(.subheadline.weight(.semibold))
                            Text(flag.note).font(.subheadline)
                            SourceLinks(urls: flag.sources)
                        }
                    }
                }
            }
            Section("Medicines to be careful with") {
                if herb.interactions.isEmpty {
                    Text("No documented interactions found.").foregroundStyle(.secondary)
                }
                ForEach(herb.interactions.sorted { $0.severity > $1.severity }, id: \.self) { it in
                    VStack(alignment: .leading, spacing: 3) {
                        HStack {
                            Text(data.label(for: it.drugClass)).font(.subheadline.weight(.semibold))
                            Spacer()
                            Text(it.severity.title).font(.caption2.bold()).foregroundStyle(it.severity.color)
                        }
                        Text(it.effect).font(.subheadline)
                        SourceLinks(urls: it.sources)
                    }
                }
            }
            if !herb.commonProducts.isEmpty {
                Section("Common products") {
                    Text(herb.commonProducts.joined(separator: ", ")).font(.footnote).foregroundStyle(.secondary)
                }
            }
        }
        .navigationTitle(herb.name)
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Shared pieces

private struct SourceLinks: View {
    let urls: [String]

    var body: some View {
        HStack(spacing: 10) {
            ForEach(Array(urls.prefix(3).enumerated()), id: \.offset) { index, string in
                if let url = URL(string: string) {
                    Link("Source \(index + 1)", destination: url).font(.caption)
                }
            }
        }
    }
}

struct DisclaimerText: View {
    let text: String

    var body: some View {
        Label {
            Text(text).font(.footnote)
        } icon: {
            Image(systemName: "info.circle").foregroundStyle(.orange)
        }
    }
}

/// ContentUnavailableView is iOS 17+; this keeps the screen working on iOS 16.
private struct ContentUnavailableCompat: View {
    let title: String
    let message: String

    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: "exclamationmark.triangle").font(.largeTitle).foregroundStyle(.secondary)
            Text(title).font(.headline)
            Text(message).font(.subheadline).foregroundStyle(.secondary).multilineTextAlignment(.center)
        }
        .padding()
    }
}

extension Severity {
    var color: Color {
        switch self {
        case .major: return .red
        case .moderate: return .orange
        case .minor: return .secondary
        }
    }
}

struct AyurvedaHomeView_Previews: PreviewProvider {
    static var previews: some View {
        AyurvedaHomeView().environmentObject(AyurvedaStore())
    }
}
