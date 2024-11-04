import { Component, Input } from "@angular/core";

@Component({
	selector: "box",
	standalone: true,
	imports: [],
	templateUrl: "./box.component.html",
	styleUrl: "./box.component.scss",
})
export class BoxComponent {
	@Input() title: string = "Unknown";
}
