import { Component, Input, OnInit } from "@angular/core";
import { TableSizerDirective } from "../table-sizer.directive";
import { DBService } from "../db.service";

@Component({
	selector: "box",
	standalone: true,
	imports: [TableSizerDirective],
	templateUrl: "./box.component.html",
	styleUrl: "./box.component.scss",
})
export class BoxComponent implements OnInit {
	@Input() title: string = "Unknown";
	metrics: any = null;

	constructor(private dbService: DBService) {}

	ngOnInit() {
		this.dbService.retrieveData(this.title).subscribe({
			next: (data) => {
				this.metrics = JSON.parse(data);
			},
			error: (error) => {
				console.error('Error retrieving data', error)
				this.metrics = null;
			}
		});
	}
}
