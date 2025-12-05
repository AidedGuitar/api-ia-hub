import { useFormik } from "formik";
import React, { useState } from "react";
import { RegisterIntereface } from "./interface";
import { resgisterSchema } from "@/schemas/register.schema";
import AuthenticationServices from "@/services/authentication";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

export default function RegisterForm() {
	const [isLoading, setIsLoading] = useState(false);
	//const [showPassword, setShowPassword] = useState(false);
	const router = useRouter();

	const onSubmit = async (values: RegisterIntereface) => {
		const authenticationServices = new AuthenticationServices();
		setIsLoading(true);

		const toastId = toast.loading("Enviando datos...");

		try {
			const response = await authenticationServices.postRegister(values);

			if (response.status === 200) {
				toast.success("Su registro ha sido exitoso.", { id: toastId });
				router.push("/login");
			} else if (response.status === 409) {
				toast.error("El correo ya se encuentra registrado.", {
					id: toastId,
				});
			} else {
				toast.error("Error al registrarse.", { id: toastId });
			}
		} catch (error) {
			console.log("Error registro: ", error);
		} finally {
			setIsLoading(false);
		}
	};

	const { values, errors, touched, handleChange, handleBlur, handleSubmit } =
		useFormik({
			initialValues: {
				use_name: "",
				use_email: "",
				password: "",
				confirm_password: "",
				use_career: "",
				use_academic_level: "",
			},
			validationSchema: resgisterSchema,
			onSubmit,
		});

	return (
		<form
			onSubmit={handleSubmit}
			className="grid grid-cols-2 gap-4 w-full justify-items-center justify-center">
			<div className="flex flex-col gap-1 w-full">
				<label htmlFor="use_name" className="font-medium text-lg">
					Nombre completo
				</label>
				<input
					id="use_name"
					name="use_name"
					type="text"
					value={values.use_name}
					onChange={handleChange}
					onBlur={handleBlur}
					placeholder="Nombre completo"
					className="px-3 py-2 placeholder:text-gray-500 outline-none ring ring-edtech-blue-500 focus:ring-2 rounded-md"
				/>
				{errors.use_name && touched.use_name && (
					<p className="text-sm text-edtech-error-500">
						{errors.use_name}
					</p>
				)}
			</div>

			<div className="flex flex-col gap-1 w-full">
				<label htmlFor="use_email" className="font-medium text-lg">
					Correo
				</label>
				<input
					id="use_email"
					name="use_email"
					type="text"
					value={values.use_email}
					onChange={handleChange}
					onBlur={handleBlur}
					placeholder="you@example.com"
					className="px-3 py-2 placeholder:text-gray-500 outline-none ring ring-edtech-blue-500 focus:ring-2 rounded-md"
				/>
				{errors.use_email && touched.use_email && (
					<p className="text-sm text-edtech-error-500">
						{errors.use_email}
					</p>
				)}
			</div>

			<div className="flex flex-col gap-1 w-full">
				<label htmlFor="password" className="font-medium text-lg">
					Contraseña
				</label>
				<input
					id="password"
					name="password"
					type="text"
					value={values.password}
					onChange={handleChange}
					onBlur={handleBlur}
					placeholder="Ingresa 8 caracteres o más"
					className="px-3 py-2 placeholder:text-gray-500 outline-none ring ring-edtech-blue-500 focus:ring-2 rounded-md"
				/>
				{errors.password && touched.password && (
					<p className="text-sm text-edtech-error-500">
						{errors.password}
					</p>
				)}
			</div>

			<div className="flex flex-col gap-1 w-full">
				<label
					htmlFor="confirm_password"
					className="font-medium text-lg">
					Confirmar contraseña
				</label>
				<input
					id="confirm_password"
					name="confirm_password"
					type="text"
					value={values.confirm_password}
					onChange={handleChange}
					onBlur={handleBlur}
					placeholder="Ingresa 8 caracteres o más"
					className="px-3 py-2 placeholder:text-gray-500 outline-none ring ring-edtech-blue-500 focus:ring-2 rounded-md"
				/>
				{errors.confirm_password && touched.confirm_password && (
					<p className="text-sm text-edtech-error-500">
						{errors.confirm_password}
					</p>
				)}
			</div>

			<div className="flex flex-col gap-1 w-full">
				<label htmlFor="use_name" className="font-medium text-lg">
					Carrera
				</label>
				<select
					id="use_career"
					name="use_career"
					value={values.use_career}
					onChange={handleChange}
					onBlur={handleBlur}
					className="px-3 py-2 placeholder:text-gray-500 outline-none ring ring-edtech-blue-500 focus:ring-2 rounded-md">
					<option value="">Seleccione una carrera</option>
					<option value="ingenieria">Ingeniería</option>
					<option value="licenciatura">Licenciatura</option>
					<option value="maestria">Maestría</option>
				</select>
				{errors.use_career && touched.use_career && (
					<p className="text-sm text-edtech-error-500">
						{errors.use_career}
					</p>
				)}
			</div>

			<div className="flex flex-col gap-1 w-full">
				<label
					htmlFor="use_academic_level"
					className="font-medium text-lg">
					Nivel de estudios
				</label>
				<select
					id="use_academic_level"
					name="use_academic_level"
					value={values.use_academic_level}
					onChange={handleChange}
					onBlur={handleBlur}
					className="px-3 py-2 placeholder:text-gray-500 outline-none ring ring-edtech-blue-500 focus:ring-2 rounded-md">
					<option value="">Seleccione su nivel de estudios</option>
					<option value="bachillerato">Bachillerato</option>
					<option value="pregrado">Pregrado</option>
					<option value="licenciatura">Profesional</option>
				</select>
				{errors.use_academic_level && touched.use_academic_level && (
					<p className="text-sm text-edtech-error-500">
						{errors.use_academic_level}
					</p>
				)}
			</div>

			<button
				name="submit"
				type="submit"
				disabled={isLoading}
				className="bg-edtech-blue-800 hover:bg-edtech-blue-700 disabled:bg-edtech-blue-300 rounded-md py-2 text-bismark-950 disabled:text-bismark-400 text-white font-medium disabled:cursor-not-allowed cursor-pointer col-span-2 w-1/2">
				Registrarse
			</button>
		</form>
	);
}
