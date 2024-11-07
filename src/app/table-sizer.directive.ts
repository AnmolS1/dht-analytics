import { Directive, ElementRef, AfterViewInit, OnDestroy } from '@angular/core';

@Directive({
	selector: '[tableSizer]',
	standalone: true
})
export class TableSizerDirective implements AfterViewInit, OnDestroy {
	private observer!: MutationObserver;
	private resizeTimeout: any;

	constructor(private el: ElementRef) { }

	ngAfterViewInit() {
		this.setupObserver();
	}

	ngOnDestroy() {
		if (this.observer) {
			this.observer.disconnect();
		}
		if (this.resizeTimeout) {
			clearTimeout(this.resizeTimeout);
		}
	}

	private setupObserver() {
		this.observer = new MutationObserver((mutations) => {
			mutations.forEach((mutation) => {
				if (mutation.type === 'childList') {
					this.checkAndAdjustTables();
				}
			});
		});

		const config = { childList: true, subtree: true };
		this.observer.observe(this.el.nativeElement, config);

		this.checkAndAdjustTables();
	}

	private checkAndAdjustTables() {
		if (this.resizeTimeout) {
			clearTimeout(this.resizeTimeout);
		}

		this.resizeTimeout = setTimeout(() => {
			const table1 = this.el.nativeElement.querySelector('#metricsTable') as HTMLTableElement;
			const table2 = this.el.nativeElement.querySelector('#dataPoints') as HTMLTableElement;

			if (table1 && table2) {
				this.adjustTableWidths(table1, table2);
				this.observer.disconnect();
			}
		}, 100);
	}

	private adjustTableWidths(table1: HTMLTableElement, table2: HTMLTableElement) {
		if (table1.rows.length === 0 || table2.rows.length === 0) return;

		const table1Cells = table1.rows[0].cells;
		const table2Cells = table2.rows[0].cells;

		if (table1Cells.length < 2 || table2Cells.length < 2) return;

		const w1 = table1Cells[0].offsetWidth;
		const w2 = table1Cells[1].offsetWidth;

		table2Cells[0].style.width = `${w1}px`;
		table2Cells[1].style.width = `${w2}px`;

		table2.style.width = `${table1.offsetWidth}px`;
	}
}