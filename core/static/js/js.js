document.addEventListener("DOMContentLoaded", () => {
  const q = (sel) => document.querySelector(sel);

  const sign_in_btn = q("#sign-in-btn");
  const sign_up_btn = q("#sign-up-btn");
  const container = q(".container");

  if (sign_up_btn) {
    sign_up_btn.addEventListener("click", (e) => {
      e.preventDefault();
      container.classList.add("sign-up-mode");
    });
  }

  if (sign_in_btn) {
    sign_in_btn.addEventListener("click", (e) => {
      e.preventDefault();
      container.classList.remove("sign-up-mode");
    });
  }

  // Toggle password
  window.mostrarContraseñas = function () {
    const pass = q("#contraseña");
    const confirm = q("#confirmar_contraseña");
    const check = q("#mostrarContraseña");

    if (check.checked) {
      pass.type = "text";
      confirm.type = "text";
    } else {
      pass.type = "password";
      confirm.type = "password";
    }
  };

  // -------- VALIDACIÓN SOLO PARA SWEETALERT --------
  function validarRegistroCampos() {
    const nombre = q("#nombre")?.value.trim();
    const correo = q("#correo")?.value.trim();
    const pass = q("#contraseña")?.value;
    const confirm = q("#confirmar_contraseña")?.value;

    let errores = [];

    if (!nombre) errores.push("El nombre es obligatorio");
    if (!correo) errores.push("El correo es obligatorio");

    if (!pass) {
      errores.push("La contraseña es obligatoria");
    } else {
      if (!/[a-z]/.test(pass))
        errores.push("La contraseña debe tener al menos una letra minúscula");
      if (!/[A-Z]/.test(pass))
        errores.push("La contraseña debe tener al menos una letra mayúscula");
      if (/^[A-Za-z0-9]*$/.test(pass))
        errores.push("La contraseña debe tener al menos un carácter especial");
    }

    if (!confirm) {
      errores.push("Debe confirmar la contraseña");
    } else if (pass !== confirm) {
      errores.push("Las contraseñas no coinciden");
    }

    return errores;
  }

  // ------------------- LOGIN -------------------
  const loginForm = q("#loginForm");

  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const formData = new FormData(loginForm);
      formData.append("login", "true");

      Swal.fire({
        title: "Iniciando sesión...",
        didOpen: () => Swal.showLoading(),
        allowOutsideClick: false,
        showConfirmButton: false,
      });

      fetch("", {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then((r) => r.json())
        .then((data) => {
          Swal.close();
          Swal.fire({
            icon: data.success ? "success" : "error",
            title: data.success ? "Bienvenido" : "Error",
            text: data.message,
          }).then(() => {
            if (data.success) window.location.href = data.redirect_url;
          });
        })
        .catch(() => {
          Swal.close();
          Swal.fire("Error", "No se pudo conectar al servidor", "error");
        });
    });
  }

  // ------------------- REGISTRO -------------------
  const registerForm = q("#registerForm");

  if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const errores = validarRegistroCampos();

      if (errores.length > 0) {
        Swal.fire({
          icon: "error",
          title: "¡Campos incompletos o incorrectos!",
          html: `
              <ul style="text-align: left; font-size: 15px; margin-top: 10px;">
                ${errores.map((e) => `<li>${e}</li>`).join("")}
              </ul>
          `,
        });
        return;
      }

      const formData = new FormData(registerForm);
      formData.append("register", "true");

      Swal.fire({
        title: "Creando cuenta...",
        didOpen: () => Swal.showLoading(),
        allowOutsideClick: false,
        showConfirmButton: false,
      });

      fetch("", {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then((r) => r.json())
        .then((data) => {
          Swal.close();

          if (data.success) {
            Swal.fire({
              icon: "success",
              title: "Registro exitoso",
              text: data.message,
              timer: 2000,
              showConfirmButton: false,
            }).then(() => (window.location.href = "/login/"));
          } else {
            Swal.fire("Error", data.message, "error");
          }
        })
        .catch(() => {
          Swal.close();
          Swal.fire("Error", "No se pudo conectar al servidor", "error");
        });
    });
  }
});
