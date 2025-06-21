export interface ArticleCreate {
  wikipedia_title: string;
  wikipedia_url: string; 
  processed_summary: string;
  word_count: number;
  frequent_words: [string, number][];
  
  sentiment_polarity?: number | null;
  sentiment_subjectivity?: number | null;
  sentiment_label?: string | null;
  personal_notes?: string | null;

  user_id: number; 
}

export interface ArticleUpdate {
  personal_notes?: string | null;
}

export interface ArticleInDB extends ArticleCreate {
  id: number;
  created_at: string | null;
  saved_at: string | null;
}