export interface CoverageCheckRequest {
  claim_description: string;
  policy_id: string;
  customer_id?: string;
  claim_id?: string;
  question?: string;
}

export interface Citation {
  document: string;
  page?: number;
  clause_title?: string;
  text?: string;
}

export interface CoverageCheckResponse {
  decision: "covered" | "not_covered" | "needs_review" | "unknown";
  confidence: number;
  reasoning: string;
  citations: Citation[];
  fraud_score?: number;
  next_action: string;
}
