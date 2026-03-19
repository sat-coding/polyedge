"use client"

export default function LineChart({ values, color = "#00E676", height = 120 }: { values: number[]; color?: string; height?: number }) {
  const width = 720
  const safe = values.length ? values : [0]
  const min = Math.min(...safe)
  const max = Math.max(...safe)
  const range = Math.max(max - min, 1)
  const points = safe
    .map((v, i) => {
      const x = (i / Math.max(safe.length - 1, 1)) * width
      const y = height - ((v - min) / range) * height
      return `${x},${y}`
    })
    .join(" ")

  return (
    <svg viewBox={`0 0 ${width} ${height}`} style={{ width: "100%", height, background: "#12121A", border: "1px solid #1E1E2E", borderRadius: 10 }}>
      <polyline fill="none" stroke={color} strokeWidth="3" points={points} />
    </svg>
  )
}
