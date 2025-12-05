"use client";

import { UserIcon } from "@/assets";
import AuthenticationServices from "@/services/authentication";
import UserServices from "@/services/user";
import getFormat from "@/utils/format";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export interface UserInterface {
	use_name: string;
	use_email: string;
	use_career: string;
	use_academic_level: string;
	use_rol_id: string;
	id: string;
}

export default function Navbar() {
	const pathname = usePathname().split("/").pop();
	const router = useRouter();

	const [userData, setDataUser] = useState<UserInterface | string>(
		{} as UserInterface
	);
	const [openMenuUser, setOpenMenuUser] = useState(false);

	const userServices = new UserServices();
	const authServices = new AuthenticationServices();

	async function getIdUser() {
		const response = await fetch("/api/login", { method: "GET" });

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.message);
		}

		const dataUser = await userServices.getUserByEmail(data.sub);

		setDataUser(dataUser);
	}

	const handleCloseSession = () => {
		authServices.postLogout();
		router.push("/login");
	};

	useEffect(() => {
		getIdUser();
	}, []);

	return (
		<nav
			className={
				pathname === "login" || pathname === "registro"
					? "hidden"
					: "border-b-2 border-neutral-300 items-center bg-white"
			}>
			<div className="max-w-[1024px] w-full mx-auto px-8 py-3 flex justify-end items-center relative">
				{typeof userData === "string" ? (
					<button className="p-1 rounded-full border border-neutral-300 cursor-pointer bg-neutral-200">
						<UserIcon className="h-7 w-7" />
					</button>
				) : (
					<div className="relative">
						<button
							onClick={() => {
								setOpenMenuUser(!openMenuUser);
							}}
							className="flex gap-1.5 items-center cursor-pointer rounded-full border p-1 bg-neutral-100">
							<UserIcon className="h-5 w-5" />
						</button>
						{openMenuUser &&
							SubMenuUser(userData, handleCloseSession)}
					</div>
				)}
			</div>
		</nav>
	);
}

function SubMenuUser(userData: UserInterface, handleCloseSession: () => void) {
	return (
		<div className="absolute right-0 top-9 z-10 flex flex-col bg-white border rounded-md border-neutral-300 shadow-2xl min-w-[220px] text-sm">
			<div className="border-b border-b-neutral-300 px-4 py-3">
				<p>{getFormat(userData.use_name).capitalize}</p>
			</div>
			<div className="border-b border-b-neutral-300 px-4 py-3">
				{getFormat(userData.use_email).capitalize}
			</div>
			<div className="border-b border-b-neutral-300 px-4 py-3">
				{getFormat(userData.use_career).capitalize}
			</div>
			<button
				onClick={handleCloseSession}
				className="border-b border-b-neutral-300 px-4 py-3 text-start cursor-pointer">
				Cerrar sesión
			</button>
		</div>
	);
}
