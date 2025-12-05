import { singInSchema } from "@/schemas";
import AuthenticationServices from "@/services/authentication";
import { useFormik } from "formik";
import { useRouter } from "next/navigation";
import { useState } from "react";
import toast from "react-hot-toast";

interface SingInInterface {
	use_email: string;
	password: string;
}

export default function LoginForm() {
	const [isLoading, setIsLoading] = useState(false);
	//const [showPassword, setShowPassword] = useState(false);
	const router = useRouter();

	const onSubmit = async (values: SingInInterface) => {
		const authenticationServices = new AuthenticationServices();
		setIsLoading(true);

		const toastId = toast.loading("iniciado sesión...");

		try {
			const token = await authenticationServices.postLogin(values);

			if (token.status === 200) {
				toast.success("Inicio de sesión exitoso", { id: toastId });
				router.push("/");
			} else if (token.status === 401) {
				toast.error("Correo o contraseña incorrecto", { id: toastId });
			} else {
				toast.error("Error al iniciar sesión", { id: toastId });
			}
		} catch (error) {
			console.log("Error login: ", error)
		} finally {
			setIsLoading(false);
		}
	};

	const { values, errors, touched, handleChange, handleBlur, handleSubmit } =
		useFormik({
			initialValues: {
				use_email: "",
				password: "",
			},
			validationSchema: singInSchema,
			onSubmit,
		});

	return (
		<form onSubmit={handleSubmit} className="flex flex-col gap-3 w-full">
			<div className="flex flex-col gap-1">
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
					disabled={isLoading}
					placeholder="you@example.com"
					className="px-3 py-2 placeholder:text-gray-500 outline-none ring ring-edtech-blue-500 focus:ring-2 rounded-md"
				/>
				{errors.use_email && touched.use_email && (
					<p className="text-base text-edtech-error-500">
						{errors.use_email}
					</p>
				)}
			</div>

			<div className="flex flex-col gap-1">
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
					disabled={isLoading}
					placeholder="Ingresa 8 caracteres o m&aacute;s"
					className="px-3 py-2 placeholder:text-gray-500 outline-none ring ring-edtech-blue-500 focus:ring-2 rounded-md"
				/>
				{errors.password && touched.password && (
					<p className="text-sm text-edtech-error-500">
						{errors.password}
					</p>
				)}
			</div>

			<button
				name="submit"
				type="submit"
				disabled={isLoading}
				className="bg-edtech-blue-800 hover:bg-edtech-blue-600 disabled:bg-edtech-blue-300 rounded-md py-2 disabled:text-bismark-400 text-white font-medium disabled:cursor-not-allowed cursor-pointer">
				Ingresar
			</button>
		</form>
	);
}
