import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl text-center">
        <h1 className="text-4xl font-bold mb-4">Claim Pilot</h1>
        <p className="text-lg text-gray-600 mb-8">
          AI-powered insurance coverage analysis. Submit a claim for instant
          coverage decisions powered by agentic RAG workflows.
        </p>
        <Link
          href="/coverage-check"
          className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg text-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Check Coverage
        </Link>
      </div>
    </main>
  );
}
