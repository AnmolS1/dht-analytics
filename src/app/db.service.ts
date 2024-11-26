import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable, of } from "rxjs";
import { map, catchError } from "rxjs/operators";
import { CookieService } from "./cookie.service";

@Injectable({
	providedIn: "root",
})
export class DBService {
	constructor(
		private http: HttpClient,
		private cookieService: CookieService,
	) {}

	retrieveData(type: string): Observable<any> {
		const cookieData = this.cookieService.getCookie(type);

		if (cookieData) {
			return of(JSON.parse(cookieData));
		}

		return this.http.post("/api/update-data", { type }).pipe(
			map((response) => {
				const data = JSON.stringify(response);
				const expirationDate = this.getNextHourDate(type);
				this.cookieService.setCookie(type, data, expirationDate);
				return response;
			}),
			catchError((error) => {
				console.error("Error retrieving data:", error);
				return of(null);
			}),
		);
	}

	// last30Minutes(): Observable<any> {
	// 	return this.http.get("/api/retrieve-last-30-minutes").pipe(
	// 		map((response) => {
	// 			const data = JSON.stringify(response);
	// 			const expirationDate = this.getNextHourDate("Last 30 Minutes");
	// 			this.cookieService.setCookie(
	// 				"Last 30 Minutes",
	// 				data,
	// 				expirationDate,
	// 			);
	// 			return response;
	// 		}),
	// 		catchError((error) => {
	// 			console.error("Error retrieving data:", error);
	// 			return of(null);
	// 		}),
	// 	);
	// }

	private getNextHourDate(type: string): Date {
		const now = new Date();
		let date = new Date(now);

		if (type !== "Last 30 Minutes") {
			date.setDate(date.getDate() + 1);
			date.setHours(1, 1, 0, 0);

			if (date <= now) {
				date.setDate(date.getDate() + 1);
			}
		} else {
			const minutes = date.getMinutes();
			if (minutes < 30) {
				date.setMinutes(30, 0);
			} else {
				date.setHours(date.getHours() + 1, 5, 0, 0);
			}
		}

		return date;
	}
}
