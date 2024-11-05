import { Component, Input } from "@angular/core";
import { TableSizerDirective } from "../table-sizer.directive";

@Component({
	selector: "box",
	standalone: true,
	imports: [TableSizerDirective],
	templateUrl: "./box.component.html",
	styleUrl: "./box.component.scss",
})
export class BoxComponent {
	@Input() title: string = "Unknown";
}
