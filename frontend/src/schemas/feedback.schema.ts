import * as yup from "yup";

export const feedbackSchema = yup.object({
	fee_rating: yup
		.number()
		.required("La calificación es requerida")
		.max(5, "La calificación debe ser de 0 a 5")
		.min(0, "La calificación debe ser de 0 a 5")
		.integer("La calificación debe ser de 0 a 5"),

	fee_comment: yup
		.string()
		.optional()
		.min(3, "Mínimo 3 caracteres")
		.max(255, "Máximo 255 caracteres"),
});
