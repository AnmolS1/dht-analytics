import { Directive, ElementRef } from '@angular/core';

@Directive({
	selector: '[tableSizer]',
	standalone: true
})
export class TableSizerDirective {

	constructor(private el: ElementRef) { }

	ngAfterViewInit() {
		this.adjustTableWidths();
	}

	private adjustTableWidths() {
		const table1 = this.el.nativeElement.querySelector('#metricsTable');
		const table2 = this.el.nativeElement.querySelector('#dataPoints');

		if (!table1 || !table2)
			return;

		const table1Cells = table1.rows[0].cells;
		const table2Cells = table2.rows[0].cells;

		const w1 = table1Cells[0].offsetWidth;
		const w2 = table1Cells[1].offsetWidth;

		table2Cells[0].style.width = `${w1}px`;
		table2Cells[1].style.width = `${w2}px`;
		
		table2.style.width = `${table1.offsetWidth}px`;
	}

}
