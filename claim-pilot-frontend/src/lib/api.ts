import { CoverageCheckRequest, CoverageCheckResponse } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:9010";

export async function checkCoverage(
  request: CoverageCheckRequest
): Promise<CoverageCheckResponse> {
  const response = await fetch(
    `${API_URL}/api/v1/agentic-rag/coverage-check`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    }
  );

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}
