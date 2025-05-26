const API_BASE_URL = "https://fullstack-authentication-web-app-with.onrender.com"; // Endereço do servidor backend

async function login() {
    let user = document.getElementById('email').value;
    let pass = document.getElementById('password').value;

    let response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: user, password: pass }),
        credentials: "include" // Importante para gerenciar cookies de sessão
    });

    let data = await response.json();

    if (response.ok) {
        sessionStorage.setItem("sessionUser", data.username);
        window.location.href = "../../pages/home.html";
    } else {
        alert(data.error || "Usuário ou senha incorretos!");
    }
}

async function getTestUser() {
    let response = await fetch(`${API_BASE_URL}/get_test_user`, { 
        method: "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        }
    });

    let data = await response.json();
    if (response.ok) {
        document.getElementById('test-user-username').innerHTML = data.username;
    } else {
        document.getElementById('test-user-username').innerHTML = "test_user@mail.com";
    }
}

if (window.location.pathname.includes("index.html")) getTestUser();

// let response = await fetch(`${API_BASE_URL}/get_test_user`, { 
//     method: "GET",
//     credentials: "include",
//     headers: {
//         "Content-Type": "application/json"
//     }
// });

// let data = await response.json();
// if (response.ok) {
//     document.getElementById('test-user-username').innerHTML = data.username;
// } else {
//     document.getElementById('test-user-username').innerHTML = "test_user@mail.com";
// }
