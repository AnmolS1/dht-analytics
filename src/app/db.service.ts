import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
	providedIn: 'root'
})
export class DBService {
	constructor(private http: HttpClient) { }
	
	retrieveData(type: string): Observable<any> {
		return this.http.post(`/api/retrieve-data`, { type });
	}
}
