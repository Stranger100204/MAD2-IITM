export function saveToken(token){
    localStorage.setItem("token", token);
}

export function getToken(){
    return localStorage.getItem("token");
}

export function logout(){

    localStorage.removeItem("token");

    localStorage.removeItem("role");
}

export function saveRole(role){
    localStorage.setItem("role", role);
}

export function getRole(){
    return localStorage.getItem("role");
}