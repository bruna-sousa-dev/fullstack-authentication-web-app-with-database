const API_BASE_URL = "https://fullstack-authentication-web-app-with.onrender.com"; // Endereço do servidor backend

async function hello() {
    let response = await fetch(`${API_BASE_URL}/hello_world`, { 
        method: "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        }
    });

    let data = await response.json();
    if (response.ok) {
        document.getElementById('hello-world-response').innerHTML = data.message;
        document.getElementById('hello-world-response').style.visibility = 'visible';
    } else {
        document.getElementById('hello-world-response').innerHTML = "Erro na requisição.";
        document.getElementById('hello-world-response').style.visibility = 'visible';
    }
}

async function checkSession() {
    let response = await fetch(`${API_BASE_URL}/check_session`, { 
        method: "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        }
    });

    let data = await response.json();
    if (!response.ok && !data.logged_in) {
        window.location.href = "../../index.html";
    } else if (response.ok && data.logged_in) {
        document.getElementById('check-session-response').innerHTML = `Logado como ${data.username}`;
        document.getElementById('check-session-response').style.visibility = 'visible';
    }
}

async function debugSession() {
    let response = await fetch(`${API_BASE_URL}/debug_session`, { 
        method: "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        }
    });

    let data = await response.json();
    if (response.ok && data.session != {}) {
        document.getElementById('debug-session-response').innerHTML = data.session._user_id;
        document.getElementById('debug-session-response').style.visibility = 'visible';
    } else {
        document.getElementById('debug-session-response').innerHTML = "Erro na requisição.";
        document.getElementById('debug-session-response').style.visibility = 'visible';
    }
}

async function listUsers() {
    let response = await fetch(`${API_BASE_URL}/users`, { 
        method: "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        }
    });

    let data = await response.json();
    if (response.ok) {
        document.getElementById('users-response').innerHTML = data.users;
        document.getElementById('users-response').style.visibility = 'visible';
    } else {
        document.getElementById('users-response').innerHTML = "Erro na requisição.";
        document.getElementById('users-response').style.visibility = 'visible';
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
        document.getElementById('get-test-user-response').innerHTML = data.username;
        document.getElementById('get-test-user-response').style.visibility = 'visible';
    } else {
        document.getElementById('get-test-user-response').innerHTML = "Erro na requisição.";
        document.getElementById('get-test-user-response').style.visibility = 'visible';
    }
}

async function editUser() {
    let currentUser = sessionStorage.getItem("sessionUser");
    if (!currentUser) {
        window.location.href = "../../index.html";
        return;
    }

    let response = await fetch(`${API_BASE_URL}/edit_user/${currentUser}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: currentUser, password: "123" }),
        credentials: "include",
    });
    let data = await response.json();
    if (response.unauthorized) {
        document.getElementById('edit-user-respons').innerHTML = data.unauthorized;
        document.getElementById('edit-user-respons').style.visibility = 'visible';
    } else {
        document.getElementById('edit-user-respons').innerHTML = "Erro na requisição.";
        document.getElementById('edit-user-respons').style.visibility = 'visible';
    }

}

async function registerUser() {
    let response = await fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: "test_user_other@mail.com", password: "123456789" })
    });

    let data = await response.json();
    if (response.unauthorized) {
        document.getElementById('register-response').innerHTML = data.unauthorized;
        document.getElementById('register-response').style.visibility = 'visible';
    } else {
        document.getElementById('register-response').innerHTML = "Erro na requisição.";
        document.getElementById('register-response').style.visibility = 'visible';
    }
}

async function delUser() {
    let response = await fetch(`${API_BASE_URL}/del_user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: "test_user@mail.com" })
    });

    let data = await response.json();
    if (response.unauthorized) {
        document.getElementById('del-user-response').innerHTML = data.unauthorized;
        document.getElementById('del-user-response').style.visibility = 'visible';
    } else {
        document.getElementById('del-user-response').innerHTML = "Erro na requisição.";
        document.getElementById('del-user-response').style.visibility = 'visible';
    }
}

async function logout() {
    await fetch(`${API_BASE_URL}/logout`, {
        method: "GET",
        credentials: "include"
    });

    sessionStorage.removeItem("sessionUser");
    window.location.href = "./index.html";
}

async function visitRepo() {
    window.open('https://github.com/bruna-sousa-dev/fullstack-authentication-web-app-with-database', '_blank');
}

if (window.location.pathname.includes("home.html")) checkSession();
