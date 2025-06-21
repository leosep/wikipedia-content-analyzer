import React, { useState } from 'react';
import useDebounce from '../hooks/useDebounce';

interface SearchBarProps {
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const debouncedSearchQuery = useDebounce(searchQuery, 500);

  React.useEffect(() => {
    if (debouncedSearchQuery) { 
      onSearch(debouncedSearchQuery); 
    }
  }, [debouncedSearchQuery, onSearch]); 

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Buscar artículos en Wikipedia..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
    </div>
  );
};

export default SearchBar;