import { useState } from 'react'

const initialIncidents = [
  {
    id: 'INC-003',
    title: 'Multiple failed login attempts',
    source: '198.51.100.23',
    severity: 'High',
    status: 'Open',
  },
  {
    id: 'INC-002',
    title: 'Suspicious authentication activity',
    source: '192.0.2.20',
    severity: 'Medium',
    status: 'Investigating',
  },
  {
    id: 'INC-001',
    title: 'Security monitoring initialized',
    source: 'Local system',
    severity: 'Low',
    status: 'Resolved',
  },
]

const navItems = [
  { icon: '◈', label: 'Overview' },
  { icon: '⚑', label: 'Incidents' },
  { icon: '⌕', label: 'AI Investigation' },
  { icon: '▧', label: 'Evidence Analysis' },
  { icon: '⌘', label: 'GitHub Security' },
]

function StatCard({ label, value, note, icon, color = 'text-cyan-300' }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-[#0d1524] p-5">
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm text-slate-400">{label}</span>
        <span className={`text-xl ${color}`}>{icon}</span>
      </div>
      <p className="mt-5 text-2xl font-semibold text-white">{value}</p>
      <p className="mt-2 text-xs text-slate-500">{note}</p>
    </div>
  )
}

function SeverityBadge({ severity }) {
  const styles = {
    High: 'bg-rose-400/10 text-rose-300',
    Medium: 'bg-amber-400/10 text-amber-300',
    Low: 'bg-emerald-400/10 text-emerald-300',
  }

  return (
    <span className={`rounded-full px-2.5 py-1 text-xs ${styles[severity] || styles.Low}`}>
      {severity}
    </span>
  )
}

function App() {
  const [activePage, setActivePage] = useState('Overview')
  const [query, setQuery] = useState('')
  const [investigation, setInvestigation] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [fileMessage, setFileMessage] = useState('')

  async function handleInvestigation(event) {
    event.preventDefault()

    if (!query.trim()) {
      setInvestigation('Enter a security question first.')
      return
    }

    setLoading(true)
    setInvestigation('The investigation API has not been connected yet. This is a dashboard preview.')

    setLoading(false)
  }

  function handleFileChange(event) {
    const file = event.target.files?.[0]

    setSelectedFile(file || null)
    setFileMessage(
      file
        ? `${file.name} selected. Upload and analysis will be enabled when the backend is connected.`
        : '',
    )
  }

  const pageDescriptions = {
    Overview: 'Monitor incidents and investigate suspicious activity.',
    Incidents: 'Review detected security incidents and their status.',
    'AI Investigation': 'Ask questions about threats and security events.',
    'Evidence Analysis': 'Prepare screenshots and visual evidence for analysis.',
    'GitHub Security': 'Connect repository security information and GitHub findings.',
  }

  return (
    <div className="min-h-screen bg-[#080d18] text-slate-200">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-64 border-r border-slate-800 bg-[#0b1220] p-5 lg:block">
        <div className="mb-10 flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-cyan-400/10 text-2xl text-cyan-300">
            ⌘
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-wide text-white">
              CyberGuard <span className="text-cyan-300">AI</span>
            </h1>
            <p className="text-xs text-slate-500">Autonomous security platform</p>
          </div>
        </div>

        <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-widest text-slate-500">
          Workspace
        </p>

        <nav className="space-y-1">
          {navItems.map(({ icon, label }) => (
            <button
              key={label}
              onClick={() => setActivePage(label)}
              className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm transition ${
                activePage === label
                  ? 'border border-cyan-400/20 bg-cyan-400/10 text-cyan-300'
                  : 'text-slate-400 hover:bg-slate-800/70 hover:text-white'
              }`}
            >
              <span className="w-5 text-lg">{icon}</span>
              {label}
            </button>
          ))}
        </nav>

        <div className="absolute bottom-5 left-5 right-5 rounded-xl border border-slate-800 bg-slate-900/70 p-4">
          <div className="mb-2 flex items-center gap-2 text-sm font-medium text-white">
            <span className="h-2 w-2 rounded-full bg-amber-400" />
            Development mode
          </div>
          <p className="text-xs leading-5 text-slate-500">
            Preview dashboard. Live backend status will be checked after API integration.
          </p>
        </div>
      </aside>

      <main className="min-h-screen lg:ml-64">
        <header className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 bg-[#0b1220]/80 px-5 py-5 sm:px-8">
          <div>
            <p className="text-xs uppercase tracking-widest text-slate-500">
              Security operations center
            </p>
            <h2 className="mt-1 text-xl font-semibold text-white">{activePage}</h2>
            <p className="mt-1 text-sm text-slate-400">{pageDescriptions[activePage]}</p>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-300">
            <span className="h-2 w-2 rounded-full bg-amber-400" />
            Backend not connected
          </div>
        </header>

        <div className="space-y-7 p-5 sm:p-8">
          {activePage === 'Overview' && (
            <>
              <section className="relative overflow-hidden rounded-2xl border border-cyan-400/20 bg-gradient-to-br from-cyan-950/60 via-[#111c30] to-[#111827] p-6 sm:p-8">
                <div className="relative z-10 max-w-2xl">
                  <p className="text-sm font-medium tracking-widest text-cyan-300">
                    CYBERGUARD INTELLIGENCE
                  </p>
                  <h3 className="mt-3 text-3xl font-bold leading-tight text-white sm:text-4xl">
                    Security insights.
                    <br />
                    Powered by AI.
                  </h3>
                  <p className="mt-4 max-w-xl text-sm leading-6 text-slate-400">
                    Monitor security incidents, investigate suspicious activity, and analyze
                    visual evidence from one workspace.
                  </p>
                  <button
                    onClick={() => setActivePage('AI Investigation')}
                    className="mt-6 rounded-xl bg-cyan-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300"
                  >
                    Open AI investigation →
                  </button>
                </div>

                <div className="pointer-events-none absolute -right-10 -top-16 h-72 w-72 rounded-full border border-cyan-300/10 sm:right-12">
                  <div className="absolute inset-8 rounded-full border border-cyan-300/15">
                    <div className="absolute inset-8 rounded-full border border-cyan-300/20" />
                  </div>
                </div>
              </section>

              <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                <StatCard
                  label="Tracked incidents"
                  value="3"
                  note="Sample preview data"
                  icon="▤"
                />
                <StatCard
                  label="Open incidents"
                  value="1"
                  note="Not yet fetched from PostgreSQL"
                  icon="⚑"
                  color="text-rose-300"
                />
                <StatCard
                  label="AI investigation"
                  value="Ready"
                  note="Ollama + RAG module developed"
                  icon="✳"
                  color="text-violet-300"
                />
                <StatCard
                  label="Evidence analysis"
                  value="Ready"
                  note="Vision module developed"
                  icon="▧"
                  color="text-emerald-300"
                />
              </section>

              <section className="grid gap-6 xl:grid-cols-5">
                <div className="overflow-hidden rounded-2xl border border-slate-800 bg-[#0d1524] xl:col-span-3">
                  <div className="flex items-center justify-between border-b border-slate-800 px-5 py-4">
                    <div>
                      <h3 className="font-semibold text-white">Recent incidents</h3>
                      <p className="mt-1 text-xs text-slate-500">
                        Example records — live data connection pending
                      </p>
                    </div>
                    <button
                      onClick={() => setActivePage('Incidents')}
                      className="text-sm text-cyan-300 hover:text-cyan-200"
                    >
                      View all →
                    </button>
                  </div>

                  <div className="overflow-x-auto">
                    <table className="w-full min-w-[540px] text-left text-sm">
                      <thead className="bg-slate-900/60 text-xs uppercase tracking-wide text-slate-500">
                        <tr>
                          <th className="px-5 py-3 font-medium">Incident</th>
                          <th className="px-5 py-3 font-medium">Severity</th>
                          <th className="px-5 py-3 font-medium">Status</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/80">
                        {initialIncidents.map((incident) => (
                          <tr key={incident.id} className="hover:bg-slate-800/30">
                            <td className="px-5 py-4">
                              <p className="font-medium text-slate-200">{incident.title}</p>
                              <p className="mt-1 text-xs text-slate-500">
                                {incident.id} · {incident.source}
                              </p>
                            </td>
                            <td className="px-5 py-4">
                              <SeverityBadge severity={incident.severity} />
                            </td>
                            <td className="px-5 py-4 text-xs text-slate-400">
                              {incident.status}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                <div className="rounded-2xl border border-slate-800 bg-[#0d1524] p-5 xl:col-span-2">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-400/10 text-xl text-violet-300">
                      ✳
                    </div>
                    <div>
                      <h3 className="font-semibold text-white">AI security investigator</h3>
                      <p className="text-xs text-slate-500">RAG + LangGraph + Ollama</p>
                    </div>
                  </div>

                  <p className="mt-5 text-sm leading-6 text-slate-400">
                    Ask a question about suspicious activity or a security incident.
                  </p>

                  <form onSubmit={handleInvestigation} className="mt-4 space-y-3">
                    <textarea
                      value={query}
                      onChange={(event) => setQuery(event.target.value)}
                      placeholder="What should I check after repeated failed logins?"
                      rows={4}
                      className="w-full resize-y rounded-xl border border-slate-700 bg-[#080d18] p-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-cyan-400"
                    />
                    <button
                      disabled={loading}
                      className="w-full rounded-xl bg-violet-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-violet-400 disabled:opacity-50"
                    >
                      {loading ? 'Preparing…' : 'Start investigation →'}
                    </button>
                  </form>

                  {investigation && (
                    <p className="mt-4 rounded-xl border border-violet-400/20 bg-violet-400/5 p-3 text-sm leading-6 text-violet-200">
                      {investigation}
                    </p>
                  )}
                </div>
              </section>
            </>
          )}

          {activePage === 'Incidents' && (
            <section className="overflow-hidden rounded-2xl border border-slate-800 bg-[#0d1524]">
              <div className="border-b border-slate-800 px-5 py-4">
                <h3 className="font-semibold text-white">Incident queue</h3>
                <p className="mt-1 text-xs text-slate-500">
                  Sample records only. Connect the API to load real incidents.
                </p>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full min-w-[600px] text-left text-sm">
                  <thead className="bg-slate-900/60 text-xs uppercase tracking-wide text-slate-500">
                    <tr>
                      <th className="px-5 py-3 font-medium">ID</th>
                      <th className="px-5 py-3 font-medium">Incident</th>
                      <th className="px-5 py-3 font-medium">Source</th>
                      <th className="px-5 py-3 font-medium">Severity</th>
                      <th className="px-5 py-3 font-medium">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/80">
                    {initialIncidents.map((incident) => (
                      <tr key={incident.id}>
                        <td className="px-5 py-4 text-slate-500">{incident.id}</td>
                        <td className="px-5 py-4 font-medium text-white">{incident.title}</td>
                        <td className="px-5 py-4 text-slate-400">{incident.source}</td>
                        <td className="px-5 py-4">
                          <SeverityBadge severity={incident.severity} />
                        </td>
                        <td className="px-5 py-4 text-slate-400">{incident.status}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

          {activePage === 'AI Investigation' && (
            <section className="max-w-3xl rounded-2xl border border-slate-800 bg-[#0d1524] p-6">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-violet-400/10 text-2xl text-violet-300">
                  ✳
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">AI investigation workspace</h3>
                  <p className="text-sm text-slate-500">Retrieval-augmented security analysis</p>
                </div>
              </div>
              <form onSubmit={handleInvestigation} className="mt-6 space-y-4">
                <label htmlFor="investigation-query" className="block text-sm text-slate-300">
                  Investigation question
                </label>
                <textarea
                  id="investigation-query"
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  rows={5}
                  placeholder="Describe the suspicious event or ask a security question..."
                  className="w-full rounded-xl border border-slate-700 bg-[#080d18] p-4 text-sm text-white outline-none placeholder:text-slate-600 focus:border-violet-400"
                />
                <button
                  disabled={loading}
                  className="rounded-xl bg-violet-500 px-5 py-3 text-sm font-semibold text-white hover:bg-violet-400 disabled:opacity-50"
                >
                  {loading ? 'Preparing investigation…' : 'Run investigation'}
                </button>
              </form>
              {investigation && (
                <div className="mt-5 rounded-xl border border-violet-400/20 bg-violet-400/5 p-4 text-sm leading-6 text-violet-200">
                  {investigation}
                </div>
              )}
              <p className="mt-5 text-xs leading-5 text-slate-500">
                This interface is a preview. The next integration step will send questions to your
                existing FastAPI investigation endpoint.
              </p>
            </section>
          )}

          {activePage === 'Evidence Analysis' && (
            <section className="max-w-3xl rounded-2xl border border-slate-800 bg-[#0d1524] p-6">
              <h3 className="text-lg font-semibold text-white">Visual evidence analysis</h3>
              <p className="mt-2 text-sm leading-6 text-slate-400">
                Select a screenshot or security image to prepare it for analysis. Uploading and AI
                processing are not connected in this preview.
              </p>
              <label
                htmlFor="evidence-file"
                className="mt-6 flex cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-slate-700 bg-[#080d18] p-10 text-center transition hover:border-cyan-400/50"
              >
                <span className="text-3xl text-cyan-300">▧</span>
                <span className="mt-3 text-sm font-medium text-white">
                  Choose an evidence image
                </span>
                <span className="mt-2 text-xs text-slate-500">PNG, JPEG, or WEBP</span>
                <input
                  id="evidence-file"
                  type="file"
                  accept="image/png,image/jpeg,image/webp"
                  onChange={handleFileChange}
                  className="mt-4 max-w-full text-sm text-slate-400"
                />
              </label>
              {selectedFile && (
                <p className="mt-4 break-words text-sm text-slate-300">
                  Selected: {selectedFile.name}
                </p>
              )}
              {fileMessage && (
                <p className="mt-3 rounded-xl bg-slate-800/60 p-3 text-sm text-slate-300">
                  {fileMessage}
                </p>
              )}
            </section>
          )}

          {activePage === 'GitHub Security' && (
            <section className="max-w-3xl rounded-2xl border border-slate-800 bg-[#0d1524] p-6">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-700/40 text-2xl text-white">
                  ⌘
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">GitHub security integration</h3>
                  <p className="text-sm text-slate-500">Repository and API connectivity</p>
                </div>
              </div>
              <div className="mt-6 rounded-xl border border-slate-800 bg-[#080d18] p-4">
                <p className="text-sm font-medium text-slate-200">Repository</p>
                <p className="mt-2 break-all text-sm text-cyan-300">
                  https://github.com/aleena431/CyberGuard-AI
                </p>
                <p className="mt-3 text-xs leading-5 text-slate-500">
                  Repository hosting is configured. Live repository security data has not been
                  connected to this page yet.
                </p>
              </div>
            </section>
          )}

          <footer className="flex flex-wrap justify-between gap-2 border-t border-slate-800 pt-5 text-xs text-slate-600">
            <span>CyberGuard AI · Development preview</span>
            <span>Local development environment</span>
          </footer>
        </div>
      </main>
    </div>
  )
}

export default App