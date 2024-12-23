import React, { useState, useEffect } from 'react';

const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT || 'http://localhost:3000/snippets';

const SnippetForm = ({ snippet = {}, onSave }) => {
  const [formData, setFormData] = useState({
    title: '',
    code: '',
    language: '',
    description: '',
  });

  const [apiError, setApiError] = useState('');

  const [errors, setErrors] = useState([]);

  useEffect(() => {
    if (snippet.id) {
      setFormData({
        title: snippet.title,
        code: snippet.code,
        language: snippet.language,
        description: snippet.description,
      });
    }
  }, [snippet]);

  const validateForm = () => {
    const newErrors = [];
    if (!formData.title) newErrors.push("Title is required.");
    if (!formData.code) newErrors.push("Code snippet is required.");
    if (!formData.language) newErrors.push("Programming language is required.");
    setErrors(newErrors);
    return newErrors.length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setApiError('');

    if (!validateForm()) return;

    try {
      const response = await fetch(`${API_ENDPOINT}`, {
        method: snippet.id ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || 'Network response was not ok');
      }

      onSave();
    } catch (error) {
      console.error("Failed to save the snippet:", error);
      setApiError(error.message);
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      {errors.length > 0 && (
        <ul>{errors.map((error, index) => <li key={index}>{error}</li>)}</ul>
      )}
      {apiError && <div className="api-error">{apiError}</div>}
      <div>
        <label htmlFor="title">Title:</label>
        <input type="text" id="title" name="title" value={formData.title} onChange={handleChange} required />
      </div>
      <div>
        <label htmlFor="code">Code:</label>
        <textarea id="code" name="code" value={formData.code} onChange={handleChange} required />
      </div>
      <div>
        <label htmlFor="language">Language:</label>
        <input type="text" id="language" name="language" value={formData.language} onChange={handleChange} required />
      </div>
      <div>
        <label htmlFor="description">Description:</label>
        <textarea id="description" name="description" value={formData.description} onChange={handleChange} />
      </div>
      <button type="submit">Save Snippet</button>
    </form>
  );
};

export default SnippetForm;