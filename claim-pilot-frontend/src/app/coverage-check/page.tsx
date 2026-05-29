"use client";

import { useState } from "react";
import { checkCoverage } from "@/lib/api";
import { CoverageCheckResponse } from "@/types";

export default function CoverageCheckPage() {
  const [claimDescription, setClaimDescription] = useState("");
  const [policyId, setPolicyId] = useState("");
  const [claimId, setClaimId] = useState("");
  const [question, setQuestion] = useState("Is this claim covered?");
  const [result, setResult] = useState<CoverageCheckResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await checkCoverage({
        claim_description: claimDescription,
        policy_id: policyId,
        claim_id: claimId || undefined,
        question,
      });
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  }

  const decisionColor = {
    covered: "text-green-700 bg-green-50 border-green-200",
    not_covered: "text-red-700 bg-red-50 border-red-200",
    needs_review: "text-yellow-700 bg-yellow-50 border-yellow-200",
    unknown: "text-gray-700 bg-gray-50 border-gray-200",
  };

  return (
    <main className="min-h-screen p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Coverage Check</h1>

      <form onSubmit={handleSubmit} className="space-y-4 mb-8">
        <div>
          <label className="block text-sm font-medium mb-1">
            Claim Description *
          </label>
          <textarea
            value={claimDescription}
            onChange={(e) => setClaimDescription(e.target.value)}
            className="w-full border rounded-lg p-3 min-h-[100px] text-gray-900"
            placeholder="Describe the claim incident..."
            required
            minLength={10}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">
              Policy ID *
            </label>
            <input
              type="text"
              value={policyId}
              onChange={(e) => setPolicyId(e.target.value)}
              className="w-full border rounded-lg p-3 text-gray-900"
              placeholder="AUTO-12345"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Claim ID</label>
            <input
              type="text"
              value={claimId}
              onChange={(e) => setClaimId(e.target.value)}
              className="w-full border rounded-lg p-3 text-gray-900"
              placeholder="CLM-1001"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Question</label>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full border rounded-lg p-3 text-gray-900"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Check Coverage"}
        </button>
      </form>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 mb-4">
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-4">
          <div
            className={`p-4 border rounded-lg ${decisionColor[result.decision]}`}
          >
            <div className="flex justify-between items-center">
              <span className="text-lg font-bold uppercase">
                {result.decision.replace("_", " ")}
              </span>
              <span className="text-sm">
                Confidence: {(result.confidence * 100).toFixed(0)}%
              </span>
            </div>
          </div>

          <div className="p-4 border rounded-lg">
            <h3 className="font-semibold mb-2">Reasoning</h3>
            <p className="text-gray-700">{result.reasoning}</p>
          </div>

          {result.fraud_score !== null && result.fraud_score !== undefined && (
            <div className="p-4 border rounded-lg">
              <h3 className="font-semibold mb-2">Fraud Score</h3>
              <p className="text-gray-700">
                {(result.fraud_score * 100).toFixed(0)}% risk
              </p>
            </div>
          )}

          {result.citations.length > 0 && (
            <div className="p-4 border rounded-lg">
              <h3 className="font-semibold mb-2">Citations</h3>
              <ul className="space-y-2">
                {result.citations.map((citation, i) => (
                  <li key={i} className="text-sm text-gray-700">
                    <span className="font-medium">{citation.document}</span>
                    {citation.page && ` (p. ${citation.page})`}
                    {citation.clause_title && ` — ${citation.clause_title}`}
                    {citation.text && (
                      <p className="mt-1 text-gray-500 italic">
                        {citation.text}
                      </p>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="p-4 border rounded-lg">
            <h3 className="font-semibold mb-2">Next Action</h3>
            <p className="text-gray-700">{result.next_action}</p>
          </div>
        </div>
      )}
    </main>
  );
}
