"use client";
import Typewriter from "typewriter-effect";

const TypeEffect = ({ message }: { message: string }) => {
	return (
		<Typewriter
			onInit={(typewriter) => {
				typewriter
					.typeString(message) // Directement la chaîne de caractères
					.callFunction(() => {
						const cursorElement = document.querySelector(
							".Typewriter__cursor"
						) as HTMLElement;
						if (cursorElement) {
							cursorElement.style.display = "none";
						}
					})
					.start();
			}}
			options={{ delay: 5, skipAddStyles: true }}
		/>
	);
};

export default TypeEffect;
