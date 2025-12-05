import * as yup from "yup";

export const singInSchema = yup.object({
	use_email: yup
		.string()
		.required("El correo es requerido")
		.email("El correo electrónico no es válido")
		.matches(
			/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
			"El correo electrónico no es válido"
		)
		.max(255, "Máximo 255 caracteres")
		.trim(),

	password: yup
		.string()
		.required("La contraseña es obligatoria")
		.matches(
			/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-ZñÑ0-9!@#$%^&*(),.?":{}|<>]+$/,
			"La contraseña debe contener al menos una letra minúscula, una mayúscula, un número y no puede tener espacios"
		)
		.min(8, "La contraseña requiere minimo 8 caracteres")
		.trim(),
});
