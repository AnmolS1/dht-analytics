import { Component } from "@angular/core";
import { RouterOutlet } from "@angular/router";
import { BoxComponent } from "./box/box.component";

@Component({
	selector: "app-root",
	standalone: true,
	imports: [RouterOutlet, BoxComponent],
	templateUrl: "./app.component.html",
	styleUrl: "./app.component.scss",
})
export class AppComponent {
	title = "HumTum Metrics";
}
