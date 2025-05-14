import { useFormik } from "formik";
import { signIn } from "next-auth/react";
import { useEffect } from "react";

export default function LoginForm() {
	const onSubmit = async (e: any) => {
		e.preventDefault();
		const { email, password } = values;

		await signIn("credentials", {
			email,
			password,
			callbackUrl: "/",
		});
	};

	const { values, errors, touched, handleChange, handleBlur } = useFormik({
		initialValues: {
			email: "",
			password: "",
		},
		onSubmit,
	});

	return (
		<form action="" onSubmit={onSubmit} className="flex flex-col gap-3">
			<label htmlFor="" className="flex flex-col gap-1">
				<span>Correo</span>
				<input
					id="email"
					name="email"
					type="text"
					onChange={handleChange}
					onBlur={handleBlur}
					placeholder="you@example.com"
					className="px-3 py-2 placeholder:text-gray-500 outline-none ring ring-bismark-400 focus:ring-2 rounded-md"
				/>
			</label>

			<label htmlFor="" className="flex flex-col gap-1">
				<span>Contraseña</span>
				<input
					id="password"
					name="password"
					type="text"
					onChange={handleChange}
					onBlur={handleBlur}
					placeholder="Ingresa 6 caracteres o m&aacute;s"
					className="px-3 py-2 placeholder:text-gray-500 outline-none ring ring-bismark-400 focus:ring-2 rounded-md"
				/>
			</label>

			<button
				name="submit"
				type="submit"
				disabled={!values.email || !values.password}
				className="bg-bismark-200 hover:bg-bismark-300 active:bg-bismark-400 disabled:bg-bismark-100 rounded-md py-2 text-bismark-950 disabled:text-bismark-400">
				Ingresar
			</button>
		</form>
	);
}
