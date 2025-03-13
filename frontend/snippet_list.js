import React, { useState, useEffect } from 'react';
import axios from 'axios';
const CodeSnippetList = () => {
  const [snippets, setSnippets] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/code-snippets`);
        setSnippets(response.data);
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };
    fetchData();
  }, []);
  const handleSnippetClick = (id) => {
    console.log(`Snippet with ID ${id} was clicked`);
  };
  return (
    <div className="snippet-list">
      {snippets.length > 0 ? (
        snippets.map((snippet) => (
          <div key={snippet.id} onClick={() => handleSnippetClick(snippet.id)} className="snippet-item">
            <h3>{snippet.title}</h3>
            <p>Language: {snippet.language}</p>
            <p>{snippet.description}</p>
          </div>
        ))
      ) : (
        <p>Loading snippets...</p>
      )}
    </div>
  );
};
export default CodeSnippetList;