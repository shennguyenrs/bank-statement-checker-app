<script lang="ts">
	import qs from 'qs';
	import type { PageData } from './$types';
	import { API_BASE_URL, API_TOKEN } from '$lib/constants';

	export let data: PageData;
	$: rows = data.data.rows;
	$: description = '';
	$: sortBy = 'date.asc';
	$: pageSize = 10;
	$: currentPage = 1;
	$: totalPages = data.data.totalPages ?? 0;

	function formatMontery(amount: number) {
		return amount.toLocaleString('vi-VN');
	}

	async function handleFilter(page: number) {
		const sortParts = sortBy.split('.');
		const query = qs.stringify(
			{
				page,
				pageSize,
				description,
				sortBy: sortParts[0],
				sort: sortParts[1]
			},
			{
				encodeValuesOnly: true
			}
		);

		const url = `${API_BASE_URL}/statements?${query}`;
		const res = await fetch(url, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${API_TOKEN}`
			}
		});
		const data = await res.json();

		// Map response to frontend
		rows = data.rows;
		totalPages = data.totalPages;
		pageSize = data.pageSize;
		sortBy = `${data.sortBy}.${data.sort}`;
	}

	async function goToPage(page: number) {
		currentPage = page;
		await handleFilter(page);
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
			<option value="date.desc">Date from latest</option>
			<option value="credit.desc">Amount largest to smallest</option>
			<option value="credit.asc">Amount smallest to largest</option>
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
			on:click={() => handleFilter(1)}>Filter</button
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
<div class="mt-4 flex items-center justify-between">
	<div>
		Showing {(currentPage - 1) * pageSize + 1} to {Math.min(currentPage * pageSize, totalPages)} of {totalPages}
		entries
	</div>
	<div class="flex gap-2">
		<button
			class="rounded-md bg-gray-200 px-3 py-1 disabled:opacity-50"
			on:click={() => goToPage(currentPage - 1)}
			disabled={currentPage === 1}
		>
			Previous
		</button>
		{#each Array(totalPages) as _, i}
			{#if i < 2 || i === totalPages - 1 || i + 1 === currentPage}
				<button
					class={[
						'rounded-md px-3 py-1 transition-all duration-300 ease-in-out hover:scale-105 active:scale-95',
						currentPage === i + 1 ? 'bg-zinc-800 text-white' : 'bg-gray-200'
					].join(' ')}
					on:click={() => goToPage(i + 1)}
				>
					{i + 1}
				</button>
			{:else if i === 2 || i === totalPages - 2}
				<span class="px-1">...</span>
			{/if}
		{/each}
		<button
			class="rounded-md bg-gray-200 px-3 py-1 disabled:opacity-50"
			on:click={() => goToPage(currentPage + 1)}
			disabled={currentPage === totalPages}
		>
			Next
		</button>
	</div>
</div>
