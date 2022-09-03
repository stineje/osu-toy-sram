`timescale 1ns/1ps

module tb();

  // Define signals
  localparam T = 20;

  logic         clk, reset, strobe,
  logic         rd_enb_0(rd_enb_0),
  logic [4:0]   rd_adr_0(rd_adr_0),
  logic [31:0]  rd_dat_0(rd_dat_0),
  logic         rd_enb_1(rd_enb_1),
  logic [4:0]   rd_adr_1(rd_adr_1),
  logic [31:0]  rd_dat_1(rd_dat_1),
  logic         wr_enb_0(wr_enb_0),
  logic [4:0]   wr_adr_0(wr_adr_0),
  logic [31:0]  wr_dat_0(wr_dat_0)

  // Instatiate dut (device under test)
  ra_2r1w_32x32_sdr dut (
                         .clk(clk),
                         .reset(reset),
                         .strobe(strobe),
                         .rd_enb_0(rd_enb_0),
                         .rd_adr_0(rd_adr_0),
                         .rd_dat_0(rd_dat_0),
                         .rd_enb_1(rd_enb_1),
                         .rd_adr_1(rd_adr_1),
                         .rd_dat_1(rd_dat_1),
                         .wr_enb_0(wr_enb_0),
                         .wr_adr_0(wr_adr_0),
                         .wr_dat_0(wr_dat_0)
                         );


  // input         clk;
  // input         reset;
  // input         strobe;

  // input         rd_enb_0;
  // input  [0:4]  rd_adr_0;
  // output [0:31] rd_dat_0;

  // input         rd_enb_1;
  // input  [0:4]  rd_adr_1;
  // output [0:31] rd_dat_1;

  // input         wr_enb_0;
  // input  [0:4]  wr_adr_0;
  // input  [0:31] wr_dat_0;

  // reg           rd_enb_0_q;
  // reg [0:4]     rd_adr_0_q;




  // Set up clk
  always
  begin
    clk = 1'b0;
    #(T / 2);
    clk = 1'b1;
    #(T / 2);
  end

  // Initial reset
  initial
  begin
    reset = 1;
    #(T/2);
    reset = 0;
  end

  initial
  begin
    // Initialize beginning values to 0
    strobe = 0;
               
    rd_enb_0 = 0;
    rd_adr_0 = 0;

    rd_enb_1 = 0;
    rd_adr_1 = 0;      

    wr_enb_0 = 0;      
    wr_adr_0 = 0;      
    wr_dat_0 = 0;      
    #10
    
    ///////////////////FIRST TEST/////////////////////////
    // Write in 0xAAAA (1010_1010_1010_1010) to address 0x0001
    wr_adr_0 = 32'h0001;      
    #1
    wr_dat_0 = 32'hAAAA;
    #1
    wr_enb_0 = 1'b1;      
    #5
    wr_enb_0 = 1'b0;      

    
    #10
    // After 10ns, try and read value from word line
    rd_adr_0 = 32'hAAAA;
    #1
    rd_enb_0 = 1'b1;
    #5
    rd_enb_0 = 1'b0;

    #10
    rd_adr_1 = 32'hAAAA;
    #1
    rd_enb_1 = 1'b1;
    #5
    rd_enb_1 = 1'b0;


    ///////////////////SECOND TEST/////////////////////////
    // Write in 0x8 (0000_0000_0000_1000) to address 0x0008
    wr_adr_0 = 32'h0008;      
    #1
    wr_dat_0 = 32'h0008;
    #1
    wr_enb_0 = 1'b1;      
    #5
    wr_enb_0 = 1'b0;      

    
    #10
    // After 10ns, try and read value from word line
    rd_adr_0 = 32'h0008;
    #1
    rd_enb_0 = 1'b1;
    #5
    rd_enb_0 = 1'b0;

    #10
    rd_adr_1 = 32'h0008;
    #1
    rd_enb_1 = 1'b1;
    #5
    rd_enb_1 = 1'b0;


    #100

    $stop;
  end

endmodule
