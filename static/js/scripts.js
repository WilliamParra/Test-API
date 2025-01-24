// Add new user
async function addUser() {
  const name = document.getElementById("nameInput").value;
  const age = document.getElementById("ageInput").value;
  const statusElement = document.getElementById("addStatus");

  if (!name || !age) {
    statusElement.innerHTML = `
            <div class="error">Please fill in all fields</div>
        `;
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/api/users/", {
      method: "POST", // Asegúrate de que sea POST
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: name, age: age }), // Pasar los datos en el cuerpo de la solicitud
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    statusElement.innerHTML = `
            <div class="success">User added successfully!</div>
        `;

    // Clear inputs
    document.getElementById("nameInput").value = "";
    document.getElementById("ageInput").value = "";

    // Reload user list
    //loadAllUsers();
  } catch (error) {
    statusElement.innerHTML = `
            <div class="error">Error adding user: ${error.message}</div>
        `;
  }
}

// Search users
async function searchUsers() {
  const name = document.getElementById("searchInput").value;
  const statusElement = document.getElementById("searchStatus");

  // Verifica si el campo de nombre está vacío
  if (!name) {
    statusElement.innerHTML = `
      <div class="error">Please enter a name to search</div>
    `;
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/api/users/search", {
      method: "POST", // Asegúrate de que sea POST
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: name }), // Enviar el nombre en el cuerpo
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Users data:", data);

    // Si no existe la propiedad 'results', usar directamente los datos
    const users = data.results || data; // Usar 'data' directamente si no existe 'results'

    console.log("Users:", users);

    // Verifica lo que contiene 'users' antes de pasar a displayUsers
    console.log(users); // Esto debería ser un array
    displayUsers(users);
    statusElement.innerHTML = "";
  } catch (error) {
    statusElement.innerHTML = `
      <div class="error">Error searching users: ${error.message}</div>
    `;
  }
}
// Load all users
async function loadAllUsers() {
  const statusElement = document.getElementById("searchStatus");

  try {
    const response = await fetch("http://127.0.0.1:5000/api/users/data");

    // Verificar si la respuesta fue exitosa
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("All users data:", data);  // Verificar la estructura de los datos

    if (data.error) {
      throw new Error(data.error);
    }

    // Verificar que la respuesta tenga la propiedad 'results'
    const users = data.results || [];
    displayUsers(users);
    statusElement.innerHTML = "";
  } catch (error) {
    statusElement.innerHTML = `
      <div class="error">Error loading users: ${error.message}</div>
    `;
    console.error(error);  // Para ver detalles en la consola
  }
}


// Display users in the results container
function displayUsers(users) {
  const resultsContainer = document.getElementById("resultsContainer");
  resultsContainer.innerHTML = ""; // Limpiar los resultados anteriores

  // Verifica que 'users' sea un array antes de proceder
  if (!Array.isArray(users) || users.length === 0) {
    resultsContainer.innerHTML = '<div class="user-item">No users found</div>';
    return;
  }

  users.forEach((user) => {
    const userElement = document.createElement("div");
    userElement.className = "user-item";
    userElement.innerHTML = `
      <strong>ID:</strong> ${user.id}<br>
      <strong>Name:</strong> ${user.name}<br>
      <strong>Age:</strong> ${user.age}
    `;
    resultsContainer.appendChild(userElement);
  });
}

// Load all users when page loads
//loadAllUsers();
