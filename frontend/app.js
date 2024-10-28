const API_URL = process.env.REACT_APP_API_URL;

function debounce(func, wait, immediate) {
  let timeout;
  return function() {
    let context = this, args = arguments;
    let later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    let callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};

async function fetchSnippets(page = 1, limit = 10) {
  try {
    const response = await fetch(`${API_URL}/snippets?page=${page}&limit=${limit}`);
    if (!response.ok) {
      throw new Error(`Error fetching snippets: ${response.statusText}`);
    }
    const { data, totalPages } = await response.json();
    displaySnippets(data);
    displayPagination(page, totalPages);
  } catch (error) {
    displayError(error);
  }
}

async function createSnippet(snippet) {
  try {
    const response = await fetch(`${API_URL}/snippets`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(snippet),
    });
    if (!response.ok) {
      throw new Error(`Error creating snippet: ${response.statusText}`);
    }
    fetchSnippets();
  } catch (error) {
    console.error("Creating snippet failed:", error);
  }
}

async function updateSnippet(id, updatedSnippet) {
  try {
    const response = await fetch(`${API_URL}/snippets/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedSnippet),
    });
    if (!response.ok) {
      throw new Error(`Error updating snippet: ${response.statusText}`);
    }
    fetchSnippets();
  } catch (error) {
    displayError(error);
  }
}

async function deleteSnippet(id) {
  try {
    const response = await fetch(`${API_URL}/snippets/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error(`Error deleting snippet: ${response.statusText}`);
    }
    fetchSnippets();
  } catch (error) {
    displayError(error);
  }
}

async function searchSnippets(query) {
  if (query.length < 3) {
    return;
  }
  try {
    const response = await fetch(`${API_URL}/snippets/search?query=${query}`);
    if (!response.ok) {
      throw new Error(`Error searching snippets: ${response.statusText}`);
    }
    const data = await response.json();
    displaySnippets(data);
  } catch (error) {
    displayError(error);
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

function displayPagination(currentPage, totalPages) {
  const paginationContainer = document.querySelector("#paginationContainer");
  paginationContainer.innerHTML = '';

  for (let page = 1; page <= totalPages; page++) {
    const pageButton = document.createElement("button");
    pageButton.textContent = page;
    if (page === currentPage) {
      pageButton.disabled = true;
    }
    pageButton.onclick = () => fetchSnippets(page);
    paginationContainer.appendChild(pageButton);
  }
}

function displayError(error) {
  console.error("An error occurred:", error);
  const errorContainer = document.querySelector("#errorContainer");
  errorContainer.textContent = `An error occurred: ${error.message}`;
  setTimeout(() => { errorContainer.textContent = ''; }, 5000);
}

document.addEventListener("DOMContentLoaded", () => {
  fetchSnippets();

  const createButton = document.querySelector("#createButton");
  createButton.addEventListener("click", () => {
    const snippetContent = document.querySelector("#snippetContent").value;
    createSnippet({ content: snippetContent });
  });

  const searchInput = document.querySelector("#searchInput");
  const debouncedSearch = debounce(() => {
    const query = searchInput.value.trim();
    if (query) {
      searchSnippets(query);
    } else {
      fetchSnippets();
    }
  }, 300);

  searchInput.addEventListener("input", debouncedSearch);
});