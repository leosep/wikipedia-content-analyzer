export interface WikipediaSearchArticle {
  title: string;
  pageid: number;
  url: string;
}

export interface WikipediaArticleDetail {
  title: string;
  summary: string;
  full_url: string;
  content: string;
  references: string[];
  url: string; 
  word_count: number;
  frequent_words: string[]; 
  sentiment_polarity: number;
  sentiment_subjectivity: number;
  sentiment_label: string;
}