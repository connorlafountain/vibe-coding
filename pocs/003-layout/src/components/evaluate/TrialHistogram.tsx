import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import type { TrialResult } from '@/types'

interface Props {
  trials: TrialResult[]
}

function binTrials(trials: TrialResult[], bins = 10) {
  const values = trials.map(t => t.kw_dc)
  const min = Math.min(...values)
  const max = Math.max(...values)
  if (min === max) return [{ range: `${min.toFixed(0)} kW`, count: trials.length }]
  const binWidth = (max - min) / bins
  return Array.from({ length: bins }, (_, i) => {
    const lo = min + i * binWidth
    const hi = min + (i + 1) * binWidth
    return {
      range: `${lo.toFixed(0)}`,
      count: values.filter(v => v >= lo && (i === bins - 1 ? v <= hi : v < hi)).length,
    }
  }).filter(b => b.count > 0)
}

export function TrialHistogram({ trials }: Props) {
  const data = binTrials(trials)
  return (
    <div className="p-3">
      <p className="text-xs text-muted-foreground mb-2">kW DC distribution (100 trials)</p>
      <ResponsiveContainer width={260} height={140}>
        <BarChart data={data} margin={{ top: 4, right: 4, bottom: 16, left: 0 }}>
          <XAxis dataKey="range" tick={{ fontSize: 10 }} label={{ value: 'kW DC', position: 'insideBottom', offset: -4, fontSize: 10 }} />
          <YAxis tick={{ fontSize: 10 }} width={24} />
          <Tooltip formatter={(v) => [`${v} trials`, 'Count']} />
          <Bar dataKey="count" fill="#f59e0b" radius={[2, 2, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
