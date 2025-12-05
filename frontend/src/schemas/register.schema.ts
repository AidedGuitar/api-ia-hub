import * as yup from "yup";

export const resgisterSchema = yup.object({
	use_name: yup
		.string()
		.required("El nombre de usuario es requerido")
		.min(3, "Mínimo 3 caracteres")
		.max(255, "Máximo 255 caracteres")
		.trim(),

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

	confirm_password: yup
		.string()
		.required("La contraseña es obligatoria")
		.oneOf([yup.ref("password")], "Las contraseñas no coinciden"),

	use_career: yup.string().required("La carrera es requerida").trim(),

	use_academic_level: yup
		.string()
		.required("El nivel de estudio es requerido")
		.trim(),
});
