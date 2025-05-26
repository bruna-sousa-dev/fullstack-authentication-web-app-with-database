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
        document.getElementById('debug-session-response').innerHTML = `ID do usuário: ${data.session._user_id}`;
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

        const usersResponse = document.getElementById("users-response");
        let usernamesText = "";
        for (let user of data.users) {
            usernamesText += user.username + "; ";  // <br> para pular linha
        }
        usersResponse.innerHTML = usernamesText;
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
    
    document.getElementById('edit-user-response').innerHTML = "Somente o administrador pode editar usuários! ;)";
    document.getElementById('edit-user-response').style.visibility = 'visible';
    let response = await fetch(`${API_BASE_URL}/edit_user/${currentUser}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: currentUser, password: "123" }),
        credentials: "include",
    });
    let data = await response.json();
    
}

async function registerUser() {
    document.getElementById('register-response').innerHTML = "Somente o administrador pode registrar novos usuários! ;)";
    document.getElementById('register-response').style.visibility = 'visible';
    let response = await fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: "test_user_other@mail.com", password: "123456789" })
    });
    let data = await response.json();
    
}

async function delUser() {
    document.getElementById('del-user-response').innerHTML = "Somente o administrador pode deletar usuários! ;)";
    document.getElementById('del-user-response').style.visibility = 'visible';
    let response = await fetch(`${API_BASE_URL}/del_user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: "admin@mail.com" })
    });
    let data = await response.json();
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
