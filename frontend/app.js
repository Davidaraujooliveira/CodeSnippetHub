const API_URL = process.env.REACT_APP_API_URL;

async function fetchSnippets() {
  try {
    const response = await fetch(`${API_URL}/snippets`);
    const data = await response.json();
    displaySnippets(data);
  } catch (error) {
    console.error("Fetching snippets failed:", error);
  }
}

async function createSnippet(snippet) {
  try {
    await fetch(`${API_URL}/snippets`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(snippet),
    });
    fetchSnippets();
  } catch (error) {
    console.error("Creating snippet failed:", error);
  }
}

async function updateSnippet(id, updatedSnippet) {
  try {
    await fetch(`${API_URL}/snippets/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedSnippet),
    });
    fetchSnippets();
  } catch (error) {
    console.error("Updating snippet failed:", error);
  }
}

async function deleteSnippet(id) {
  try {
    await fetch(`${API_URL}/snippets/${id}`, {
      method: 'DELETE',
    });
    fetchSnippets();
  } catch (error) {
    console.error("Deleting snippet failed:", error);
  }
}

async function searchSnippets(query) {
  try {
    const response = await fetch(`${API_URL}/snippets/search?query=${query}`);
    const data = await response.json();
    displaySnippets(data);
  } catch (error) {
    console.error("Searching snippets failed:", error);
  }
}

function displaySnippets(snippets) {
  const snippetsContainer = document.querySelector("#snippetsContainer");
  snippetsContainer.innerHTML = '';
  snippets.forEach(snippet => {
    const snippetElement = document.createElement("div");
    snippetElement.textContent = snippet.content;
    snippetsContainer.appendChild(snippetElement);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  fetchSnippets();

  const createButton = document.querySelector("#createButton");
  createButton.addEventListener("click", () => {
    const snippetContent = document.querySelector("#snippetContent").value;
    createSnippet({ content: snippetContent });
  });

  const searchInput = document.querySelector("#searchInput");
  searchInput.addEventListener("input", () => {
    const query = searchInput.value;
    searchSnippets(query);
  });
});