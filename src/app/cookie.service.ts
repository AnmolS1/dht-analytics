import { Injectable } from "@angular/core";

@Injectable({
	providedIn: "root",
})
export class CookieService {
	setCookie(name: string, value: string, expirationDate: Date) {
		document.cookie = `${name}=${value};expires=${expirationDate.toUTCString()};path=/`;
	}

	getCookie(name: string): string | null {
		const cookies = document.cookie.split(";");
		for (let cookie of cookies) {
			const [cookieName, cookieValue] = cookie
				.split("=")
				.map((c) => c.trim());
			if (cookieName === name) {
				return cookieValue;
			}
		}

		return null;
	}

	deleteCookie(name: string) {
		document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
	}
}
