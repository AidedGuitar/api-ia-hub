import { ApplicationInterface } from "@/app/page";
import { ImageIcon, StarIcon } from "@/assets";
import Link from "next/link";

export default function AppCard(item: ApplicationInterface) {
	return (
		<Link
			key={item.id}
			href={"./" + item.id}
			target="_blank"
			className="h-fit border rounded-md w-48 shadow-lg">
			<div className="p-2 justify-items-center bg-edtech-blue-100">
				<ImageIcon className="w-24 h-24" />
			</div>
			<div className="p-2 flex flex-col gap-2  border-t rounded-md">
				<div className="flex justify-between gap-4 items-start">
					<div className="flex flex-col gap-px">
						<p className="text-sm font-semibold">{item.app_name}</p>
						<p className="text-xs text-neutral-500">{item.app_category}</p>
					</div>
					<div className="text-sm flex items-center gap-px">
						<p>{Number(item.avg_rating).toFixed(1)}</p>
						<StarIcon className="w-5 h-5 fill-amber-200" />
					</div>
				</div>
				<p className="line-clamp-2 text-sm text-neutral-700">{item.app_description}</p>
			</div>
		</Link>
	);
}
