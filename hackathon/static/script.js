/**
 * BACKEND API CONNECTOR & CONTROLLER
 * Connects the Digital Lost & Found frontend directly to the FastAPI backend.
 */
const API_BASE_URL = "http://127.0.0.1:8000/api";

let currentUser = null;

// Initialize App: Fetch live data from backend when page loads
document.addEventListener("DOMContentLoaded", () => {
  fetchAndRenderItems();
  fetchAndRenderAdminTable();
});

/* ==========================================
   1. BACKEND API INTERACTIONS
   ========================================== */

// Fetch items from FastAPI backend with active search & filter query params
async function fetchAndRenderItems() {
  const searchVal = document.getElementById("searchInput").value.trim();
  const typeVal = document.getElementById("typeFilter").value;
  const categoryVal = document.getElementById("categoryFilter").value;

  const params = new URLSearchParams();
  if (searchVal) params.append("query", searchVal);
  if (categoryVal && categoryVal !== "all") params.append("category", categoryVal);
  if (typeVal && typeVal !== "all") params.append("item_type", typeVal);

  try {
    const response = await fetch(`${API_BASE_URL}/items?${params.toString()}`);
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

    const items = await response.json();
    
    // Filter by client-side date if date input is set
    const dateVal = document.getElementById("dateFilter").value;
    const finalItems = dateVal ? items.filter(i => i.date === dateVal) : items;

    renderItems(finalItems);
  } catch (error) {
    console.error("Error fetching items from API:", error);
    const grid = document.getElementById("itemsGrid");
    grid.innerHTML = `<p style="grid-column: 1/-1; text-align:center; color: var(--text-muted);">Unable to load items. Make sure your FastAPI backend is running.</p>`;
  }
}

// Fetch all items for the Admin Panel
async function fetchAndRenderAdminTable() {
  try {
    const response = await fetch(`${API_BASE_URL}/items`);
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

    const items = await response.json();
    renderAdminTable(items);
  } catch (error) {
    console.error("Error fetching admin table items:", error);
  }
}

// Post a new lost/found report to FastAPI
async function handleReportSubmit(event) {
  event.preventDefault();

  const previewImg = document.getElementById("imagePreview").src;
  
  const newItem = {
    title: document.getElementById("itemName").value,
    item_type: document.getElementById("reportType").value,
    category: document.getElementById("category").value,
    location: document.getElementById("location").value,
    date: document.getElementById("eventDate").value,
    description: document.getElementById("description").value,
    image_url: previewImg && !previewImg.endsWith("#") ? previewImg : ""
  };

  try {
    const response = await fetch(`${API_BASE_URL}/items`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newItem)
    });

    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

    alert("Report submitted successfully! It is pending admin verification.");
    
    // Reset form UI
    document.getElementById("reportForm").reset();
    document.getElementById("imagePreview").className = "hidden-preview";
    document.getElementById("uploadPlaceholder").style.display = "block";

    // Refresh views from live database
    fetchAndRenderItems();
    fetchAndRenderAdminTable();
    switchTab("browse");
  } catch (error) {
    console.error("Error submitting report:", error);
    alert("Failed to submit report. Please verify your backend server connection.");
  }
}

// Approve an item via Admin endpoint (PATCH)
async function verifyItem(itemId) {
  try {
    const response = await fetch(`${API_BASE_URL}/items/${itemId}/verify`, {
      method: "PATCH"
    });

    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

    alert("Item successfully verified and published!");
    fetchAndRenderItems();
    fetchAndRenderAdminTable();
  } catch (error) {
    console.error("Error verifying item:", error);
    alert("Could not verify item.");
  }
}

/* ==========================================
   2. UI RENDERING FUNCTIONS
   ========================================== */

function renderItems(itemsToRender) {
  const grid = document.getElementById("itemsGrid");
  grid.innerHTML = "";

  if (!itemsToRender || itemsToRender.length === 0) {
    grid.innerHTML = `<p style="grid-column: 1/-1; text-align:center; color: var(--text-muted);">No items found matching your filter criteria.</p>`;
    return;
  }

  itemsToRender.forEach(item => {
    const card = document.createElement("div");
    card.className = "item-card";

    const imageUrl = item.image_url || item.image || "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=500&auto=format&fit=crop&q=60";
    const itemType = item.item_type || item.type || "Lost";

    card.innerHTML = `
      <img src="${imageUrl}" alt="${item.title}" class="item-image">
      <div class="item-body">
        <div class="item-header">
          <span class="badge ${itemType === 'Lost' ? 'badge-lost' : 'badge-found'}">${itemType}</span>
          <small class="item-meta">${item.category}</small>
        </div>
        <h3 class="item-title">${item.title}</h3>
        <p class="item-meta">📍 ${item.location}</p>
        <p class="item-meta">📅 ${item.date}</p>
        <p class="item-desc">${item.description}</p>
        <button class="btn btn-primary btn-block" onclick="openContactModal(${item.id})">Request Contact Info</button>
      </div>
    `;
    grid.appendChild(card);
  });
}

function renderAdminTable(items) {
  const tbody = document.getElementById("adminTableBody");
  tbody.innerHTML = "";

  if (!items || items.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;">No items recorded in database.</td></tr>`;
    return;
  }

  items.forEach(item => {
    const itemType = item.item_type || item.type || "Lost";
    const itemStatus = item.status || (item.is_verified ? "approved" : "pending");

    const row = document.createElement("tr");
    row.innerHTML = `
      <td><strong>${item.title}</strong></td>
      <td><span class="badge ${itemType === 'Lost' ? 'badge-lost' : 'badge-found'}">${itemType}</span></td>
      <td>${item.category}</td>
      <td>${item.location}</td>
      <td>${item.date}</td>
      <td><span class="badge ${itemStatus === 'approved' ? 'badge-found' : 'badge-pending'}">${itemStatus}</span></td>
      <td class="action-cell">
        ${itemStatus === 'pending' ? `<button class="btn btn-success" onclick="verifyItem(${item.id})">Approve</button>` : ''}
      </td>
    `;
    tbody.appendChild(row);
  });
}

/* ==========================================
   3. FILTERS & NAVIGATION HELPERS
   ========================================== */

function filterItems() {
  fetchAndRenderItems();
}

function resetFilters() {
  document.getElementById("searchInput").value = "";
  document.getElementById("typeFilter").value = "all";
  document.getElementById("categoryFilter").value = "all";
  document.getElementById("dateFilter").value = "";
  fetchAndRenderItems();
}

function switchTab(tabName) {
  document.querySelectorAll(".tab-content").forEach(el => el.classList.remove("active"));
  document.querySelectorAll(".nav-btn").forEach(el => el.classList.remove("active"));

  if (tabName === "browse") {
    document.getElementById("browseTab").classList.add("active");
  } else if (tabName === "report") {
    document.getElementById("reportTab").classList.add("active");
  } else if (tabName === "admin") {
    document.getElementById("adminTab").classList.add("active");
    fetchAndRenderAdminTable();
  }
}

function previewImage(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const preview = document.getElementById("imagePreview");
      preview.src = e.target.result;
      preview.className = "image-preview-active";
      document.getElementById("uploadPlaceholder").style.display = "none";
    }
    reader.readAsDataURL(file);
  }
}

/* ==========================================
   4. MODALS & AUTHENTICATION
   ========================================== */

function openContactModal(itemId) {
  document.getElementById("modalItemId").value = itemId;
  document.getElementById("contactModal").classList.add("active");
}

function closeContactModal() {
  document.getElementById("contactModal").classList.remove("active");
}

async function handleContactSubmit(event) {
  event.preventDefault();
  alert("Contact request sent! The owner/finder will review your claim details.");
  closeContactModal();
  document.getElementById("contactForm").reset();
}

function openAuthModal() {
  document.getElementById("authModal").classList.add("active");
}

function closeAuthModal() {
  document.getElementById("authModal").classList.remove("active");
}

function toggleAuthMode(mode) {
  if (mode === 'login') {
    document.getElementById("loginForm").classList.add("active");
    document.getElementById("registerForm").classList.remove("active");
    document.getElementById("loginTabBtn").classList.add("active");
    document.getElementById("registerTabBtn").classList.remove("active");
  } else {
    document.getElementById("registerForm").classList.add("active");
    document.getElementById("loginForm").classList.remove("active");
    document.getElementById("registerTabBtn").classList.add("active");
    document.getElementById("loginTabBtn").classList.remove("active");
  }
}

async function handleAuth(event, type) {
  event.preventDefault();
  if (type === 'login') {
    const email = document.getElementById("loginEmail").value;
    currentUser = { email };
    document.getElementById("authBtn").textContent = `Account (${email.split('@')[0]})`;
  } else {
    const name = document.getElementById("regName").value;
    currentUser = { name };
    document.getElementById("authBtn").textContent = `Account (${name})`;
  }
  closeAuthModal();
}