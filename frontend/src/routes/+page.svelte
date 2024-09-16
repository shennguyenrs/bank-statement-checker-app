<script lang="ts">
	import qs from 'qs';

	import type { PageData } from './$types';

	export let data: PageData;
	$: rows = data.data.rows;
	$: description = '';
	$: sortBy = 'date.asc';
	$: pageSize = 10;
	$: currentPage = 1;

	function formatMontery(amount: number) {
		return amount.toLocaleString('vi-VN');
	}

	async function handleFilter() {
		const sortParts = sortBy.split('.');
		const query = qs.stringify(
			{
				page: currentPage,
				pageSize,
				description,
				sortBy: sortParts[0],
				sort: sortParts[1]
			},
			{
				encodeValuesOnly: true
			}
		);

		const url = `${import.meta.env.VITE_API_BASE_URL}/statements?${query}`;
		const res = await fetch(url, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${import.meta.env.VITE_API_TOKEN}`
			}
		});
		const data = await res.json();
		rows = data.rows;
	}
</script>

<p class="text-3xl font-bold uppercase">Bank Statement Checker</p>
<p>
	This application is used to search for records that have been imported from bank statement PDF
	files
</p>
<div class="h-10" />
<div class="flex justify-between">
	<input
		type="text"
		name="description"
		placeholder="Search keyword in description..."
		class="w-1/3 rounded-md border border-gray-50 bg-gray-50 px-2"
		bind:value={description}
	/>
	<div class="flex gap-2">
		<select
			class="rounded-md border border-gray-50 bg-gray-50 px-2"
			name="sort"
			placeholder="Sort by"
			bind:value={sortBy}
		>
			<option value="date.asc">Date from earliest</option>
			<option value="date.esc">Date from latest</option>
			<option value="credit.asc">Amount largest to smallest</option>
			<option value="credit.esc">Amount smallest to largest</option>
		</select>
		<select
			class="rounded-md border border-gray-50 bg-gray-50 px-2"
			name="size"
			placeholder="Page size"
			bind:value={pageSize}
		>
			<option value={10}>10</option>
			<option value={20}>20</option>
			<option value={50}>50</option>
		</select>
		<button
			class="rounded-md bg-zinc-800 px-4 py-2 text-white transition-all duration-300 ease-in-out hover:scale-105 hover:bg-zinc-700 active:scale-95"
			on:click={handleFilter}>Filter</button
		>
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
