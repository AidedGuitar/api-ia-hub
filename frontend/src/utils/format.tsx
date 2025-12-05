// String functions

function capitalize(word: string): string {
	if (typeof word === "undefined") return "";

	return word.slice(0, 1).toUpperCase() + word.slice(1).toLowerCase();
}

function capitalizeMin(word: string): string {
	if (typeof word === "undefined") return "";

	return word.slice(0).toLowerCase();
}

function capitalizeAll(string: string): string {
	if (typeof string === "undefined") return "";

	return string
		.split(" ")
		.map((word) => capitalize(word))
		.join(" ");
}

function initials(string: string): string {
	if (typeof string === "undefined") return "";

	const words = string.split(" ");
	let initials: string = "";

	if (words.length > 1) {
		const firstInitial = words[0].slice(0, 1);
		const lastInitial = words[words.length - 1].slice(0, 1);

		initials = `${firstInitial}${lastInitial}`;
	} else {
		initials = words[0].slice(0, 1);
	}

	return initials;
}

interface getFormatProps {
	originalValue: string;
	capitalize: string;
	capitalizeMin: string;
	capitalizeAll: string;
	initials: string;
}

export default function getFormat(value: string): getFormatProps {
	const finalFormat: getFormatProps = {
		originalValue: value,
		capitalize: capitalize(value),
		capitalizeMin: capitalizeMin(value),
		capitalizeAll: capitalizeAll(value),
		initials: initials(value),
	};

	return finalFormat;
}

// Number functions

function currency(value: number): string {
	const formatting_options: Intl.NumberFormatOptions = {
		style: "currency",
		currency: "COP",
		minimumFractionDigits: 0,
	};

	const currencyFormatter = new Intl.NumberFormat(
		"es-CO",
		formatting_options
	);
	const finalCurrency = currencyFormatter.format(value);

	return finalCurrency;
}

interface getNumberFormatProps {
	originalValue: number;
	currency: string;
}

export function getNumberFormat(value: number): getNumberFormatProps {
	const finalFormat: getNumberFormatProps = {
		originalValue: value,
		currency: currency(value),
	};

	return finalFormat;
}
