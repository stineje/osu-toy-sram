// single array plus output latches

module toysram_16x12_wrapper (
 input                 clk,
 input                 reset,
 input  [0:15]         rwl0_000,
 input  [0:15]         rwl1_000,
 input  [0:15]         wwl0_000,
 output [0:11]         rbl0_000,
 output [0:11]         rbl1_000,
 input  [0:11]         wbl0_000,
 input  [0:11]         wbl0_b_000
);

wire [0:11] rbl0_000_ra;
wire [0:11] rbl1_000_ra;

reg  [0:11] rbl0_000_q;
reg  [0:11] rbl1_000_q;

toysram_16x12 r000 (
   .RWL0(rwl0_000),
   .RWL1(rwl1_000),
   .WWL(wwl0_000),
   .RBL0(rbl0_000_ra),
   .RBL1(rbl1_000_ra),
   .WBL(wbl0_000),
   .WBLb(wbl0_b_000)
);

always @(posedge clk) begin

   rbl0_000_q <= rbl0_000_ra;
   rbl1_000_q <= rbl1_000_ra;

end

assign rbl0_000 = rbl0_000_q;
assign rbl1_000 = rbl1_000_q;

endmodule

