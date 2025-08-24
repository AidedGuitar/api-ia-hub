import { singInSchema } from "@/schemas";
import { useFormik } from "formik";

interface SingInInterface {
	email: string;
	password: string;
}

export default function LoginForm() {
	const onSubmit = async (values: SingInInterface) => {
		console.log(values);

		// await signIn("credentials", {
		// 	email,
		// 	password,
		// 	callbackUrl: "/",
		// });
	};

	const { values, errors, touched, handleChange, handleBlur, handleSubmit } =
		useFormik({
			initialValues: {
				email: "",
				password: "",
			},
			validationSchema: singInSchema,
			onSubmit,
		});

	return (
		<form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full">
			<div className="flex flex-col gap-1">
				<label htmlFor="email" className="font-medium text-lg">
					Correo
				</label>
				<input
					id="email"
					name="email"
					type="text"
					value={values.email}
					onChange={handleChange}
					onBlur={handleBlur}
					placeholder="you@example.com"
					className="px-3 py-2 placeholder:text-gray-500 outline-none ring ring-edtech-blue-500 focus:ring-2 rounded-md"
				/>
				{errors.email && touched.email && (
					<p className="text-base text-edtech-error-500">
						{errors.email}
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
					placeholder="Ingresa 6 caracteres o m&aacute;s"
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
				disabled={false}
				className="bg-edtech-blue-800 hover:bg-edtech-blue-700 disabled:bg-edtech-blue-300 rounded-md py-2 text-bismark-950 disabled:text-bismark-400 text-white font-medium disabled:cursor-not-allowed">
				Ingresar
			</button>
		</form>
	);
}
