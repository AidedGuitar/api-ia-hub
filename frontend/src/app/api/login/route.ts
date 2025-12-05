import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import jwt from "jsonwebtoken";

export async function POST(request: Request) {
	const body = await request.json();

	// Hacer login contra tu backend real
	const res = await fetch(`${process.env.NEXT_PUBLIC_AUTH_URL}/auth/login`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(body),
	});

	const data = await res.json();

	if (!res.ok) {
		return NextResponse.json(
			{ message: "Credenciales incorrectas" },
			{ status: 401 }
		);
	}

	// Guardar token en cookie
	const cookieStore = await cookies();
	cookieStore.set("access_token", data.access_token, {
		httpOnly: true,
		secure: process.env.NODE_ENV === "production",
		sameSite: "strict",
		path: "/",
		maxAge: 60 * 60 * 24 * 7, // 7 días
	});

	return NextResponse.json({ message: "Login exitoso" }, { status: 200 });
}

export async function GET() {
	const cookieStore = await cookies();
	const token = cookieStore.get("access_token")?.value;

	if (!token) {
		return Response.json({ error: "No token" }, { status: 401 });
	}

	const decoded = jwt.verify(token, process.env.JWT_SECRET!);

	return Response.json(decoded);
}
