import React from "react";

const traders = [
  {
    rank: 1,
    name: "TradingMaster",
    type: "Swing Trader",
    country: "🇺🇸",
    challenge: "$25K",
    profit: 12.5,
    winRate: "78%",
    movement: "+2",
    status: "Passed",
    avatar: "https://i.pravatar.cc/100?img=12"
  },
  {
    rank: 2,
    name: "ForexKing",
    type: "Scalper",
    country: "🇺🇸",
    challenge: "$10K",
    profit: 9.8,
    winRate: "72%",
    movement: "0",
    status: "Passed",
    avatar: "https://i.pravatar.cc/100?img=13"
  },
  {
    rank: 3,
    name: "RiskTaker",
    type: "Trend Trader",
    country: "🇺🇸",
    challenge: "$5K",
    profit: 8.7,
    winRate: "65%",
    movement: "-1",
    status: "Passed",
    avatar: "https://i.pravatar.cc/100?img=14"
  },
  {
    rank: 4,
    name: "CryptoQueen",
    type: "Swing Trader",
    country: "🇬🇧",
    challenge: "$10K",
    profit: 7.8,
    winRate: "69%",
    movement: "+5",
    status: "Active",
    avatar: "https://i.pravatar.cc/100?img=15"
  },
  {
    rank: 5,
    name: "ScalperPro",
    type: "Scalper",
    country: "🇨🇦",
    challenge: "$5K",
    profit: 6.9,
    winRate: "85%",
    movement: "0",
    status: "Active",
    avatar: "https://i.pravatar.cc/100?img=16"
  }
];

export default function Leaderboard() {
  return (
    <div className="bg-black min-h-screen text-white">
      <div className="max-w-7xl mx-auto px-6 py-16">
        {/* TITLE */}
        <h1 className="text-4xl font-semibold">Leaderboard</h1>
        <p className="text-neutral-400 mt-2">
          Track performance and compete with traders worldwide
        </p>

        {/* STATS */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-10">
          <StatCard number="1,247" label="Total Traders" />
          <StatCard number="342" label="Passed Challenges" />
          <StatCard number="27.4%" label="Success Rate" />
          <StatCard number="15,689" label="Total Trades" />
        </div>

        {/* TOP TRADERS */}
        <h2 className="text-xl font-semibold mt-16 mb-6">
          🔥 This Week's Top Traders
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <TopTrader
            title="Weekly Champion"
            name="TradingMaster"
            stat="+8.2% this week"
            avatar="https://i.pravatar.cc/100?img=12"
          />
          <TopTrader
            title="Fastest Rising"
            name="CryptoQueen"
            stat="+5 ranks"
            avatar="https://i.pravatar.cc/100?img=15"
          />
          <TopTrader
            title="Highest Win Rate"
            name="ScalperPro"
            stat="85%"
            avatar="https://i.pravatar.cc/100?img=16"
          />
        </div>

        {/* FILTERS */}
        <div className="space-y-3 mt-10">
          <select className="w-full bg-neutral-900 border border-neutral-800 rounded-lg px-4 py-3">
            <option>All Challenges</option>
          </select>
          <select className="w-full bg-neutral-900 border border-neutral-800 rounded-lg px-4 py-3">
            <option>Sort by Profit %</option>
          </select>
          <select className="w-full bg-neutral-900 border border-neutral-800 rounded-lg px-4 py-3">
            <option>All Status</option>
          </select>
        </div>

        {/* TABLE */}
        <div className="mt-10 overflow-x-auto">
          <table className="w-full text-left">
            <thead className="text-neutral-400 border-b border-neutral-800">
              <tr>
                <th className="py-3">Rank</th>
                <th>Trader</th>
                <th>Challenge</th>
                <th>Profit %</th>
                <th>Win Rate</th>
                <th>Movement</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {traders.map((t) => (
                <tr
                  key={t.rank}
                  className="border-b border-neutral-800 hover:bg-neutral-900/40 transition-colors"
                >
                  <td className="py-4">
                    {t.rank === 1 && (
                      <div className="w-8 h-8 flex items-center justify-center rounded-full bg-yellow-500 text-black font-bold">
                        🥇
                      </div>
                    )}
                    {t.rank === 2 && (
                      <div className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-300 text-black font-bold">
                        🥈
                      </div>
                    )}
                    {t.rank === 3 && (
                      <div className="w-8 h-8 flex items-center justify-center rounded-full bg-orange-500 text-black font-bold">
                        🥉
                      </div>
                    )}
                    {t.rank > 3 && (
                      <span className="text-neutral-400 font-medium">
                        {t.rank}
                      </span>
                    )}
                  </td>
                  <td>
                    <div className="flex items-center gap-3">
                      <img
                        src={t.avatar}
                        className="w-10 h-10 rounded-full"
                      />
                      <div>
                        <p className="font-medium">
                          {t.name}
                        </p>
                        <p className="text-xs text-neutral-400">
                          {t.type} {t.country}
                        </p>
                      </div>
                    </div>
                  </td>
                  <td>{t.challenge}</td>
                  <td>
                    <p className="text-emerald-400 font-medium">
                      +{t.profit}%
                    </p>
                    <div className="w-32 h-2 bg-neutral-800 rounded-full mt-1">
                      <div
                        className="h-2 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-full transition-all duration-700"
                        style={{ width: `${t.profit * 6}%` }}
                      />
                    </div>
                  </td>
                  <td>{t.winRate}</td>
                  <td className={
                    t.movement.includes("+")
                      ? "text-emerald-400"
                      : t.movement.includes("-")
                      ? "text-red-400"
                      : "text-neutral-400"
                  }>
                    {t.movement}
                  </td>
                  <td>
                    <span
                      className={
                        t.status === "Passed"
                          ? "bg-emerald-500/20 text-emerald-400 px-3 py-1 rounded-full text-xs"
                          : "bg-cyan-500/20 text-cyan-400 px-3 py-1 rounded-full text-xs"
                      }
                    >
                      {t.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* LIVE ACTIVITY FEED */}
        <div className="mt-16">
          <h3 className="text-xl font-semibold mb-4">
            📈 Recent Activity
          </h3>
          <div className="space-y-3">
            <Activity text="CryptoQueen reached +5% profit today" icon="📈" />
            <Activity text="ScalperPro entered Top 5" icon="⬆️" />
            <Activity text="DayTraderX completed evaluation" icon="✅" />
            <Activity text="ForexKing achieved new win streak" icon="🔥" />
          </div>
        </div>

        {/* CTA */}
        <div className="mt-20 bg-gradient-to-r from-emerald-900/40 to-teal-900/40 rounded-xl p-12 text-center">
          <h2 className="text-2xl font-semibold">
            Ready to Compete?
          </h2>
          <p className="text-neutral-400 mt-2">
            Start your evaluation and climb the leaderboard.
          </p>
          <button className="mt-6 bg-gradient-to-r from-emerald-500 to-teal-500 text-black px-8 py-3 rounded-lg font-semibold hover:scale-105 transition">
            Start Your Evaluation
          </button>
        </div>
      </div>
    </div>
  );
}

function StatCard({ number, label }) {
  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6 text-center hover:border-emerald-500/40 transition">
      <p className="text-3xl font-semibold">{number}</p>
      <p className="text-sm text-neutral-400 mt-2">{label}</p>
    </div>
  );
}

function TopTrader({ title, name, stat, avatar }) {
  return (
    <div className="bg-gradient-to-br from-neutral-900 to-black border border-neutral-800 rounded-xl p-6 shadow-[0_0_40px_rgba(16,185,129,0.18)] hover:shadow-[0_0_60px_rgba(16,185,129,0.25)] transition">
      <p className="text-neutral-400 text-sm">{title}</p>
      <div className="flex items-center gap-3 mt-4">
        <img
          src={avatar}
          className="w-14 h-14 rounded-full"
        />
        <p className="font-semibold">{name}</p>
      </div>
      <p className="text-emerald-400 font-semibold mt-4">
        {stat}
      </p>
      <div className="w-full h-2 bg-neutral-800 rounded-full mt-3">
        <div className="h-2 w-2/3 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-full" />
      </div>
    </div>
  );
}

function Activity({ text, icon }) {
  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-4 flex items-center gap-3">
      <span className="text-lg">{icon}</span>
      <p className="text-sm text-neutral-300">{text}</p>
    </div>
  );
}
