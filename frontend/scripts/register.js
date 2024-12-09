document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password }),
        });

        if (response.ok) {
            alert("Usuario registrado exitosamente");
            window.location.href = "login.html";
        } else {
            alert("Error al registrarse");
        }
    } catch (error) {
        console.error("Error en el registro:", error);
    }
});
