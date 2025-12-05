import { feedbackSchema } from "@/schemas/feedback.schema";
import FeedbackServices from "@/services/feedback";
import { useFormik } from "formik";
import React, { useState } from "react";
import toast from "react-hot-toast";

export interface FeedbackCreateInterface {
	fee_rating: number;
	fee_comment: string;
}

function FormFeedback({
	idApplication,
	idUser,
	refreshDataFeedback,
}: {
	idApplication: string;
	idUser: string;
	refreshDataFeedback: () => void;
}) {
	const [isLoading, setIsLoading] = useState(false);

	const onSubmit = async (values: FeedbackCreateInterface) => {
		setIsLoading(true);

		const toastId = toast.loading("Guardando comentario...");

		try {
			const feedbackServices = new FeedbackServices();

			const data = await feedbackServices.createFeedback({
				user_id: idUser,
				application_id: idApplication,
				fee_rating: values.fee_rating,
				fee_comment: values.fee_comment,
				fee_date: new Date().toISOString(),
			});

			if (data.status === 201) {
				refreshDataFeedback();
				toast.success("Comentario guardado", { id: toastId });
			}
		} catch (error: unknown) {
			if (error instanceof Error) {
				if (error.message === "401") {
					toast.error("No se pudo guardar el comentario", {
						id: toastId,
					});
				}

				if (error.message === "409") {
					toast.error("Este usuario ya realizó un comentario", {
						id: toastId,
					});
				}
			} else {
				// Manejo de errores inesperados que no son Error
				console.error("Unexpected error:", error);
				toast.error("Ocurrió un error desconocido");
			}
		} finally {
			setIsLoading(false);
		}
	};

	const { values, errors, touched, handleChange, handleBlur, handleSubmit } =
		useFormik({
			initialValues: {
				fee_rating: "" as unknown as number,
				fee_comment: "",
			},
			onSubmit,
			validationSchema: feedbackSchema,
		});

	return (
		<form onSubmit={handleSubmit}>
			<fieldset className="border p-2 rounded-md border-neutral-300 shadow-md flex flex-col gap-2">
				<legend>Califica la aplicación</legend>
				<div className="flex flex-col gap-1">
					<label htmlFor="fee_rating" className="flex gap-1 items-end">
						<span>Puntaje:</span>
						<p className="text-sm text-neutral-400">(1-5)</p>
					</label>
					<input
						type="number"
						name="fee_rating"
						value={values.fee_rating}
						onChange={handleChange}
						onBlur={handleBlur}
						className="px-3 py-2 w-24 placeholder:text-gray-500 outline-none ring ring-edtech-blue-500 focus:ring-2 rounded-md"
					/>
					{errors.fee_rating && touched.fee_rating && (
						<p className="text-sm text-edtech-error-500">
							{errors.fee_rating}
						</p>
					)}
				</div>

				<div className="flex flex-col gap-1">
					<label htmlFor="fee_comment">
						<span>Comentario:</span>
					</label>
					<textarea
						name="fee_comment"
						value={values.fee_comment}
						onChange={handleChange}
						onBlur={handleBlur}
						placeholder="Deja tu comentario..."
						className="px-3 py-2 w-full max-h-32 min-h-16 placeholder:text-gray-500 outline-none ring ring-edtech-blue-500 focus:ring-2 rounded-md"
					/>
					{errors.fee_comment && touched.fee_comment && (
						<p className="text-sm text-edtech-error-500">
							{errors.fee_comment}
						</p>
					)}
				</div>

				<button
					name="submit"
					type="submit"
					disabled={isLoading}
					className="bg-edtech-blue-800 hover:bg-edtech-blue-600 disabled:bg-edtech-blue-300 rounded-md py-2 disabled:text-bismark-400 text-white font-medium disabled:cursor-not-allowed cursor-pointer w-fit px-4">
					Enviar
				</button>
			</fieldset>
		</form>
	);
}

export default FormFeedback;
