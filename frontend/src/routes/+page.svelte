<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
	let rows = data.data.rows;

	function formatMontery(amount: number) {
		return amount.toLocaleString('vi-VN');
	}
</script>

<p class="text-3xl font-bold uppercase">Bank Statement Checker</p>
<p>
	This application is used to search for records that have been imported from bank statement PDF
	files
</p>
<div class="h-20" />
<div class="flex justify-between">
	<input type="text" name="search" placeholder="Search keyword in description..." class="w-1/3" />
	<div class="flex gap-2">
		<select name="sort" placeholder="Sort by">
			<option value="date.asc">Date from earliest</option>
			<option value="date.esc">Date from latest</option>
			<option value="credit.asc">Amount largest to smallest</option>
			<option value="credit.esc">Amount smallest to largest</option>
		</select>
		<select name="size" placeholder="Page size">
			<option value={10}>10</option>
			<option value={20}>20</option>
			<option value={50}>50</option>
		</select>
		<button>Filter</button>
	</div>
</div>
<div class="h-8" />
<table class="table-auto">
	<thead>
		<tr class="bg-gray-50 uppercase">
			<th>Date</th>
			<th>Doc No</th>
			<th>Description</th>
			<th>Amount (VND)</th>
		</tr>
	</thead>
	<tbody>
		{#each rows as row}
			<tr class="odd:bg-white even:bg-gray-50">
				<td class="py-2">{row.date}</td>
				<td>{row.docNo}</td>
				<td class="text-left">{row.description}</td>
				<td class="text-right">{formatMontery(row.credit)}</td>
			</tr>
		{/each}
	</tbody>
</table>
